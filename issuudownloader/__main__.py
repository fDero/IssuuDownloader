from .manager import *
import os

def main():
        manager = IssuuDownloadingManager(3, "https://issuu.com/scoresondemand", "log.txt")
        manager.download_every_issuu_document(os.path.curdir)

if __name__ == '__main__':
    main()