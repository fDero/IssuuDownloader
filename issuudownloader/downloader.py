from io import BytesIO

import requests
from PIL import Image
from .utils import *


class IssuuDownloader:
    def __init__(self, logging_callback=None, file_downloaded_callback=None):
        if logging_callback is None:
            logging_callback = print
        if file_downloaded_callback is None:
            file_downloaded_callback = \
                lambda document_url, document_name: (
                    print(f"File downloaded: {document_name}({document_url})"))
        self._log = logging_callback
        self._file_downloaded_callback = file_downloaded_callback

    def _get_jpeg_url_template(self, document_url):
        issuu_oembed_url = f"https://issuu.com/oembed?url={document_url}&format=json"
        response = requests.get(issuu_oembed_url, headers=download_headers(), stream=True)
        template = json.loads(response.content)['thumbnail_url']
        assert template.endswith("/page_1_thumb_medium.jpg")
        template = template[:-len("/page_1_thumb_medium.jpg")]
        self._log(f"extracted jpg-url-template: {template}")
        return template

    def download_issuu_document_as_pdf(self, document_url, document_name, download_path):
        template = self._get_jpeg_url_template(document_url)
        images = []
        index = 1
        while True:
            document_page_url = f"{template}/page_{index}.jpg"
            self._log(f"downloading jpg {document_page_url}")
            index += 1
            response = requests.get(document_page_url, headers=download_headers(), stream=True)
            if response.status_code != 200:
                break
            img = Image.open(BytesIO(response.content)).convert('RGB')
            images.append(img)
            self._log(f"finished downloading jpg {document_page_url}")
        if images:
            images[0].save(download_path, save_all=True, append_images=images[1:])
            self._file_downloaded_callback(document_url, document_name)

    def download_all_issuu_files_from_contents_pack(self, contents, download_dir):
        for document_name, document_url in contents.items():
            self.download_issuu_document_as_pdf(document_url, document_name, download_dir)