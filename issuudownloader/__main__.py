
from .log import LogFileHandler
from .cache import CacheHandler
from .manager import *
from .commandline import *
from .validation import *
from time import sleep
import sys


def main():
    cache = None
    try:
        args = parse_commandline_arguments()
        validate_commandline_args(args)
        print("Press Ctrl/Cmd + C to exit")
        sleep(0.3)
        log_file = LogFileHandler(args.output_dir)
        cache = CacheHandler(args.output_dir, args.cache)
        manager = IssuuDownloadingManager(
            number_of_threads=args.threads,
            page_url=args.page_url,
            log_file=log_file,
            cache=cache,
        )
        manager.download_every_issuu_document(args.output_dir)
    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as ve:
        print(f"Unknown error: {ve}")
    finally:
        cache is not None and cache.write_back_to_disk()
        sys.stdout.flush()


if __name__ == '__main__':
    main()