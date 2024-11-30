import os
from datetime import datetime


class LogFileHandler:
    def __init__(self, output_dir_filepath):
        self._log_file_path = os.path.join(output_dir_filepath, "log.txt")
        with open(self._log_file_path, "w") as file:
            file.write("")

    def write(self, text_to_log):
        if self._log_file_path is not None:
            with open(self._log_file_path, "a") as file:
                current_timestamp = datetime.now()
                timestamp_str = f"--{current_timestamp.strftime("%Y-%m-%d.%H:%M:%S")}.{current_timestamp.microsecond // 1000:03d}--\n"
                file.write(timestamp_str)
                file.write(text_to_log)
                file.write("\n")