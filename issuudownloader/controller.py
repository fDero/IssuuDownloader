import threading
from tqdm import tqdm
from .downloader import *
from .fetcher import *


class IssuuDownloadingManager:
    def __init__(self, number_of_threads, page_url):
        self.number_of_threads = number_of_threads
        self.page_url = page_url
        self.estimated_file_count = 50
        self.downloaded_so_far = {}
        self.page_processed_so_far = []
        self.lock = threading.Lock()
        self.active = True

    def _update_progress_bar_callback_generator(self, pbar):
        def callback(document_url, document_name):
            with self.lock:
                self.downloaded_so_far[document_name] = document_url
                pbar.update(1)
        return callback

    def _download_some_issuu_documents_in_separate_thread(self, thread_index, pbar, download_path):
        page_index = thread_index
        downloaded_files = -1
        while downloaded_files != 0 and self.active:
            page_index += self.number_of_threads
            fetcher = IssuuFetcher(logging_callback=lambda txt: None)
            downloader = IssuuDownloader(logging_callback=lambda txt: None, file_downloaded_callback=self._update_progress_bar_callback_generator(pbar))
            page_url = f"{self.page_url}/{page_index}"
            fetched_contents = fetcher.fetch_filter_and_extract_contents_from_issuu_page(page_url)
            downloader.download_all_issuu_files_from_contents_pack(fetched_contents, download_path)
            with self.lock:
                self.page_processed_so_far.append(page_url)

    def stop(self):
        self.active = False
        with self.lock:
            print("Stopped")

    def download_every_issuu_document(self, download_path):
        with tqdm(
                total=self.estimated_file_count,
                desc="Downloading",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
                position=0,
                leave=True,
                ncols=70
        ) as pbar:
            threads = []
            for i in range(self.number_of_threads):
                downloader_thread = threading.Thread(
                    target=self._download_some_issuu_documents_in_separate_thread,
                    args=(i,pbar,download_path,),
                    daemon=True
                )
                downloader_thread.start()
                threads.append(downloader_thread)
            for thread in threads:
                thread.join()