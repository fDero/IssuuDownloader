import argparse
import os


def create_command_line_arguments_parser():
    return argparse.ArgumentParser(
        description='issuudownloader - A python commandline tool to download lots of issuu-documents as pdf'
    )


def add_commandline_option_for_selecting_page_url(parser):
    parser.add_argument(
        '-p', '--page-url',
        help='url of the page to download issuu-documents from',
        type=str,
        required=True
    )


def add_commandline_option_for_selecting_output_dir(parser):
    parser.add_argument(
        '-o', '--output-dir',
        help='relative or absolute filesystem path the output directory',
        default=os.path.curdir,
        type=str
    )


def add_commandline_option_for_selecting_thread_count(parser):
    parser.add_argument(
        '-t', '--threads',
        help='integer number of threads to use during download',
        default=3,
        type=int
    )


def add_commandline_option_for_selecting_log_file(parser):
    parser.add_argument(
        '-l', '--log-file',
        help='integer number of threads to use during download',
        default="issuu-download.log",
        type=str
    )


def parse_commandline_arguments():
    parser = create_command_line_arguments_parser()
    add_commandline_option_for_selecting_page_url(parser)
    add_commandline_option_for_selecting_output_dir(parser)
    add_commandline_option_for_selecting_thread_count(parser)
    add_commandline_option_for_selecting_log_file(parser)
    args = parser.parse_args()
    return args