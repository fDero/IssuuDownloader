import json
import os
import threading


class CacheHandler:
    def __init__(self, output_dir_filepath, use_cache):
        self._cache_file_path = os.path.join(output_dir_filepath, "cache.json")
        self._lock = threading.Lock()
        if not os.path.exists(self._cache_file_path) or not use_cache:
            with open(self._cache_file_path, "w", encoding='utf-8') as cache_file:
                cache_file.write('{ "pages": [] }')
        assert os.path.isfile(self._cache_file_path)
        with open(self._cache_file_path, "r") as cache_file:
            self._json_cache_data = json.load(cache_file)

    def register_page_as_downloaded(self, page_url):
        with self._lock:
            self._json_cache_data["pages"].append(page_url)

    def is_page_already_downloaded(self, page_url):
        with self._lock:
            return page_url in self._json_cache_data["pages"]

    def write_back_to_disk(self):
        with self._lock:
            with open(self._cache_file_path, "w", encoding='utf-8') as cache_file:
                json.dump(self._json_cache_data, cache_file, indent=4)