import threading
import signal
from .downloader import *
from .fetcher import *


class IssuuDownloadingManager:
    def __init__(self, number_of_threads, page_url, log_file_path):
        self.log_file = log_file_path
        self.estimated_file_count = self.estimate_number_of_documents_in_issuu_page(page_url)
        self.number_of_threads = number_of_threads
        self.page_url = page_url
        self.downloaded_so_far = {}
        self.page_processed_so_far = []
        self.lock = threading.Lock()
        self.threads = []
        self.stop_event = threading.Event()

    def estimate_number_of_documents_in_issuu_page(self, issuu_page_url):
        print(">> Estimating total workload")
        fetcher = IssuuFetcher(self._logging_callback)
        contents = fetcher.fetch_filter_and_extract_contents_from_issuu_page(issuu_page_url)
        contents_count = len(contents)
        pagination_class = 'Pagination__pagination__inner__iHwTs__0-0-3094'
        web_page = fetcher.fetch_html_web_page(issuu_page_url)
        elements = fetcher.filter_elements_by_class(web_page, pagination_class)
        max_page_index = 1
        for element in elements:
            for child in element.children:
                text = child.text.strip()
                if text.isdigit() and int(text) > max_page_index:
                    max_page_index = int(text)
        estimated_contents_count = max_page_index * contents_count
        print(">> Estimated total number of documents in issuu page: " + str(estimated_contents_count))
        return estimated_contents_count

    def _logging_callback(self, text_to_log):
        if self.log_file is not None:
            with open(self.log_file, "a") as file:
                file.write(text_to_log)
                file.write("\n")

    def _file_downloaded_callback(self, document_url, document_name):
        with self.lock:
            self.downloaded_so_far[document_name] = document_url
            percentage = int(len(self.downloaded_so_far) / self.estimated_file_count * 100)
            print(f"[{percentage}%]\t Downloaded {document_name}")

    def _download_some_issuu_documents_in_separate_thread(self, thread_index, download_path):
        page_index = thread_index
        fetched_contents = {}
        first_time = True
        while first_time or len(fetched_contents) > 0:
            first_time = False
            if self.stop_event.is_set():
                break
            page_index += self.number_of_threads
            fetcher = IssuuFetcher(self._logging_callback)
            downloader = IssuuDownloader(self._logging_callback, self._file_downloaded_callback)
            if self.stop_event.is_set():
                break
            page_url = f"{self.page_url}/{page_index}"
            fetched_contents = fetcher.fetch_filter_and_extract_contents_from_issuu_page(page_url)
            if self.stop_event.is_set():
                break
            for document_name, document_url in fetched_contents.items():
                downloader.download_issuu_document_as_pdf(document_url, document_name, download_path)
                if self.stop_event.is_set():
                    break
            with self.lock:
                self.page_processed_so_far.append(page_url)

    def stop_gracefully(self):
        self.stop_event.set()
        with self.lock:
            print(">> Stopping... (may take a couple of seconds)")

    def monitor_user_input_and_exit_on_sigint(self):
        signal.signal(signal.SIGINT, lambda sig, frame: self.stop_gracefully())
        try:
            while not self.stop_event.is_set():
                time.sleep(0.1)
        finally:
            for thread in self.threads:
                thread.join()
            print(">> All threads stopped, Exiting...")

    def download_every_issuu_document(self, download_path):
        print(f">> Launching multiple downloading threads: {self.number_of_threads}")
        for i in range(self.number_of_threads):
            downloader_thread = threading.Thread(
                target=self._download_some_issuu_documents_in_separate_thread,
                args=(i,download_path,),
                daemon=True
            )
            downloader_thread.start()
            self.threads.append(downloader_thread)
        self.monitor_user_input_and_exit_on_sigint()