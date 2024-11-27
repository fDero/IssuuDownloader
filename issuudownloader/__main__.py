from .manager import *
import os

def main():
        manager = IssuuDownloadingManager(
            number_of_threads=3,
            page_url="https://issuu.com/scoresondemand",
            log_file_path="issuu-downloader.log",
        )
        manager.download_every_issuu_document(os.path.curdir)

if __name__ == '__main__':
    main()