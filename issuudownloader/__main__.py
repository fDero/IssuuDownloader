from requests import HTTPError
from .manager import *
from .commandline import *
from .validation import *
from time import sleep
import sys


def main():
    try:
        args = parse_commandline_arguments()
        validate_commandline_args(args)
        print("Press Ctrl/Cmd + C to exit")
        sleep(0.3)
        manager = IssuuDownloadingManager(
            number_of_threads=args.threads,
            page_url=args.page_url,
            log_file_path=args.log_file,
        )
        manager.download_every_issuu_document(args.output_dir)
    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as ve:
        print(f"Unknown error: {ve}")
    finally:
        sys.stdout.flush()


if __name__ == '__main__':
    main()
