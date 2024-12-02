from .request import *
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

    def _store_file_on_disk(self, url, output_path):
        try:
            response = get_request(url, headers=scrape_headers(), stream=True)
            response.raise_for_status()
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            self._log(f"file downloaded successfully to {output_path}")
        except (OSError, PermissionError):
            self._log(f"!!ERROR!! file cannot be written on disk")
            print(">> ERROR: FILE CANNOT BE WRITTEN ON DISK")
            print(">> (KEEPING THE THREAD ALIVE)")

    def _prepare_issuu_document_online_pdf_conversion_via_third_party_server(self, document_url):
        payload = {"url": document_url}
        response = post_request(
            url="https://backend.img2pdf.net/download-pdf",
            headers=download_init_headers(payload),
            json=payload
        )
        self._log(f"Content: {response.content}")
        self._log(f"Headers: {response.headers}")
        return json.loads(response.content)

    def _attempt_issuu_document_online_pdf_conversion_via_third_party_server(self, document_id):
        response = get_request(
            url=f"https://backend.img2pdf.net/job/{document_id}",
            headers=download_check_headers()
        )
        self._log(f"Content: {response.content}")
        self._log(f"Headers: {response.headers}")
        json_response = json.loads(response.content)
        if json_response['status'] != "succeeded":
            return None
        return json_response

    def _download_issuu_document_as_pdf_via_third_party_server(self, document_url, document_name, download_path):
        prepared_pdf_conversion = self._prepare_issuu_document_online_pdf_conversion_via_third_party_server(document_url)
        if 'outputFile' in prepared_pdf_conversion:
            return prepared_pdf_conversion['outputFile']
        task_id = prepared_pdf_conversion['id']
        while True:
            time.sleep(1)
            conversion_outcome = self._attempt_issuu_document_online_pdf_conversion_via_third_party_server(task_id)
            if conversion_outcome is not None:
                break
        converted_pdf_file_url = conversion_outcome['outputFile']
        self._store_file_on_disk(converted_pdf_file_url, download_path)
        self._file_downloaded_callback(document_url, document_name)

    def download_issuu_document_as_pdf(self, document_url, document_name, download_path):
        self._download_issuu_document_as_pdf_via_third_party_server(document_url, document_name, download_path)

    def download_all_issuu_files_from_contents_pack(self, contents, download_dir):
        for document_name, document_url in contents.items():
            self.download_issuu_document_as_pdf(document_url, document_name, download_dir)