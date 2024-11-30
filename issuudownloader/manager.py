import threading
from .downloader import *
from .fetcher import *


class IssuuDownloadingManager:
    def __init__(self, number_of_threads, page_url, log_file, cache):
        assert number_of_threads >= 1
        self._cache = cache
        self._lock = threading.Lock()
        self._logging_callback = log_file.write
        self._estimated_file_count = self.estimate_number_of_documents_in_issuu_page(page_url)
        self._number_of_threads = number_of_threads
        self._page_url = page_url
        self._downloaded_so_far = {}
        self._threads = {}

    def estimate_number_of_documents_in_issuu_page(self, issuu_page_url):
        print(">> Estimating total workload")
        fetcher = IssuuFetcher(self._logging_callback)
        issuu_page_url_first_page = issuu_page_url + "/1"
        contents = fetcher.fetch_filter_and_extract_contents_from_issuu_page(issuu_page_url_first_page)
        contents_count = len(contents)
        elements = fetcher.fetch_filter_and_extract_pagination_data_from_issuu_page(issuu_page_url)
        max_page_index = 1
        for element in elements:
            for child in element.children:
                text = child.text.strip()
                if text.isdigit() and int(text) > max_page_index:
                    max_page_index = int(text)
        estimated_contents_count = (max_page_index - 1) * contents_count
        issuu_page_url_last_page = issuu_page_url + f"/{max_page_index}"
        last_page_contents = fetcher.fetch_filter_and_extract_contents_from_issuu_page(issuu_page_url_last_page)
        last_page_contents_count = len(last_page_contents)
        estimated_contents_count += last_page_contents_count
        print(">> Estimated total number of documents in issuu page: " + str(estimated_contents_count))
        return estimated_contents_count

    def _file_downloaded_callback(self, document_url, document_name):
        self._downloaded_so_far[document_name] = document_url
        percentage = int(len(self._downloaded_so_far) / self._estimated_file_count * 100)
        print(f"[{percentage}%]\t Downloaded {document_name}")

    def _page_skipped_callback(self, page_url, fetched_contents):
        for document_name, document_url in fetched_contents.items():
            self._downloaded_so_far[document_name] = document_url
        if len(fetched_contents) > 0:
            percentage = int(len(self._downloaded_so_far) / self._estimated_file_count * 100)
            print(f"[{percentage}%]\t Cached: The whole page {page_url} has already been downloaded")

    def _download_some_issuu_documents_in_separate_thread(self, thread_index, download_path):
        page_index = thread_index
        fetched_contents = {}
        first_time = True
        while first_time or len(fetched_contents) > 0:
            first_time = False
            fetcher = IssuuFetcher(self._logging_callback)
            downloader = IssuuDownloader(self._logging_callback, self._file_downloaded_callback)
            page_url = f"{self._page_url}/{page_index}"
            fetched_contents = fetcher.fetch_filter_and_extract_contents_from_issuu_page(page_url)
            if self._cache.is_page_already_downloaded(page_url):
                self._page_skipped_callback(page_url, fetched_contents)
                break
            self._logging_callback(str(len(fetched_contents.items())))
            for document_name, document_url in fetched_contents.items():
                downloader.download_issuu_document_as_pdf(document_url, document_name, download_path)
            if len(fetched_contents) > 0:
                self._cache.register_page_as_downloaded(page_url)
            page_index += self._number_of_threads
        with self._lock:
            self._threads.pop(thread_index)
        print(">> One thread finished execution")


    def download_every_issuu_document(self, download_path):
        print(f">> Launching multiple downloading threads: {self._number_of_threads}")
        with self._lock:
            for i in range(self._number_of_threads):
                thread_index = i + 1
                downloader_thread = threading.Thread(
                    target=self._download_some_issuu_documents_in_separate_thread,
                    args=(thread_index,download_path,),
                    daemon=True
                )
                downloader_thread.start()
                self._threads[thread_index] = downloader_thread
        while not len(self._threads) == 0:
            time.sleep(0.3)