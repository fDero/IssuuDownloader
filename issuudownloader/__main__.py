from requests import HTTPError
from .manager import *
from .commandline import *
from time import sleep
import sys


def main():
    try:
        args = parse_commandline_arguments()
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
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except HTTPError as ex:
        print(f"HTTP error: {ex}")
        print("keep in mind that urls must not contain the page index")
        print("https://issuu.com/something/1 <-- not allowed")
        print("https://issuu.com/something/ <-- not allowed")
        print("https://issuu.com/something <-- ok")
    except IOError as ioe:
        print(f"Error: {ioe}")
    finally:
        sys.stdout.flush()


if __name__ == '__main__':
    main()
