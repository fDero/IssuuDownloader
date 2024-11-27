import requests
import time
import os
from .utils import *


class IssuuDownloader:
    def __init__(self, logging_callback=None, file_downloaded_callback=None):
        if logging_callback is None:
            logging_callback = print
        if file_downloaded_callback is None:
            file_downloaded_callback = \
                lambda document_url, document_name: (
                    print(f"File downloaded: {document_name}({document_url})"))
        self.log = logging_callback
        self.file_downloaded_callback = file_downloaded_callback

    def download_file(self, url, output_path):
        response = requests.get(url, headers=scrape_headers(), stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        self.log(f"file downloaded successfully to {output_path}")
        return output_path

    def prepare_issuu_document_pdf_conversion(self, document_url):
        payload = {"url": document_url}
        response = requests.post(
            url="https://backend.img2pdf.net/download-pdf",
            headers=download_init_headers(payload),
            json=payload
        )
        self.log(f"Content: {response.content}")
        self.log(f"Headers: {response.headers}")
        return json.loads(response.content)

    def attempt_issuu_document_pdf_conversion(self, document_id):
        response = requests.get(
            url=f"https://backend.img2pdf.net/job/{document_id}",
            headers=download_check_headers()
        )
        self.log(f"Content: {response.content}")
        self.log(f"Headers: {response.headers}")
        response.raise_for_status()
        json_response = json.loads(response.content)
        if json_response['status'] != "succeeded":
            return None
        return json_response

    def fetch_issuu_document_pdf_url(self, document_url):
        prepared_pdf_conversion = self.prepare_issuu_document_pdf_conversion(document_url)
        if 'outputFile' in prepared_pdf_conversion:
            return prepared_pdf_conversion['outputFile']
        task_id = prepared_pdf_conversion['id']
        while True:
            time.sleep(1)
            conversion_outcome = self.attempt_issuu_document_pdf_conversion(task_id)
            if conversion_outcome is not None:
                break
        return conversion_outcome['outputFile']

    def download_issuu_document_as_pdf(self, document_url, document_name, download_dir):
        pdf_url = self.fetch_issuu_document_pdf_url(document_url)
        file_name = document_name + '.pdf'
        download_path = os.path.join(download_dir, file_name)
        self.download_file(pdf_url, download_path)

    def download_all_issuu_files_from_contents_pack(self, contents, download_dir):
        for document_name, document_url in contents.items():
            self.download_issuu_document_as_pdf(document_url, document_name, download_dir)
            self.file_downloaded_callback(document_url, document_name)