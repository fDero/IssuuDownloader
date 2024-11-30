import os


def validate_output_directory(output_directory):
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            assert os.path.isdir(output_directory)
            assert os.access(output_directory, os.W_OK)
        test_file_path = os.path.join(output_directory, '.write_test_issuudownloader')
        with open(test_file_path, 'w') as test_file:
            test_file.write('test')
        os.remove(test_file_path)
    except (AssertionError, PermissionError, OSError):
        print("Error while validating output directory path [-o/--output-dir]")
        print("(either such directory cannot be opened in write mode, or it can't be created, or it's not a directory)")
        exit(1)


def validate_thread_number(thread_number):
    if thread_number < 1:
        print("Invalid thread number [-t/--threads]")
        print("(thread number must be greater than or equal to 1)")
        exit(1)


def validate_issuu_document_repository(issuu_page_url):
    try:
        assert isinstance(issuu_page_url, str)
        assert len(issuu_page_url) > 0
        assert issuu_page_url.startswith("https://www.issuu.com") or issuu_page_url.startswith("https://issuu.com")
        assert not issuu_page_url.endswith("/")
    except AssertionError:
        print("ill-formatted issuu-url [-p/--page-url]")
        print("(url must start with 'https://www.issuu.com' or 'https://issuu.com' and must not end with '/')")
        exit(1)


def validate_commandline_args(args):
    validate_thread_number(args.threads)
    validate_output_directory(args.output_dir)
    validate_issuu_document_repository(args.document_repository)