from .controller import *
import os
import signal

def main():
        manager = IssuuDownloadingManager(3, "https://issuu.com/scoresondemand")
        signal.signal(signal.SIGINT, lambda sig, frame: (print("Stopping..."), manager.stop()))
        manager.download_every_issuu_document(os.path.curdir)

if __name__ == '__main__':
    main()