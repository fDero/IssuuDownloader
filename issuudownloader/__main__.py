from .manager import *
from time import sleep
import os


def main():
    try:
        print("Press Ctrl/Cmd + C to exit")
        sleep(0.3)
        manager = IssuuDownloadingManager(
            number_of_threads=3,
            page_url="https://issuu.com/scoresondemand",
            log_file_path="issuu-downloader.log",
        )
        manager.download_every_issuu_document(os.path.curdir)
    except KeyboardInterrupt:
        print("Stopping...")


if __name__ == '__main__':
    main()
