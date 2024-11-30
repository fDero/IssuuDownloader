import json
import os
import threading


class CacheHandler:
    def __init__(self, output_dir_filepath):
        self._cache_file_path = os.path.join(output_dir_filepath, "cache.json")
        self._lock = threading.Lock()
        if not os.path.exists(self._cache_file_path):
            with open(self._cache_file_path, "w", encoding='utf-8') as cache_file:
                cache_file.write('{ "invalid-files": [] }')
        assert os.path.isfile(self._cache_file_path)
        with open(self._cache_file_path, "r") as cache_file:
            self._json_cache_data = json.load(cache_file)

    def is_already_downloaded(self, document_url, download_path):
        if os.path.exists(download_path):
            with self._lock:
                return not document_url in self._json_cache_data["invalid-files"]
        return False

    def mark_file_as_invalid(self, document_url):
        with self._lock:
            if not document_url in self._json_cache_data["invalid-files"]:
                self._json_cache_data["invalid-files"].append(document_url)

    def mark_file_as_valid(self, document_url):
        with self._lock:
            self._json_cache_data["invalid-files"].remove(document_url)

    def write_back_to_disk(self):
        with self._lock:
            with open(self._cache_file_path, "w", encoding='utf-8') as cache_file:
                json.dump(self._json_cache_data, cache_file, indent=4)