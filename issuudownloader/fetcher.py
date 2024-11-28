from bs4 import BeautifulSoup
from .utils import *
import requests


class IssuuFetcher:
    def __init__(self, logging_callback=None):
        if logging_callback is None:
            logging_callback = print
        self._log = logging_callback

    def _fetch_html_web_page(self, url):
        response = requests.get(url, headers=scrape_headers())
        if response.status_code < 200 or response.status_code >= 400:
            self._log(f"Fetched from {url} failed")
            self._log(f"Status code: {response.status_code}")
            self._log(f"Defaulting to empty html")
            return "<html></html>"
        else:
            self._log(f"Successfully fetched from {url}")
            return response.content

    def _filter_elements_by_class(self, web_page, class_name):
        soup = BeautifulSoup(web_page, features='html.parser')
        elements = soup.find_all(class_=class_name)
        self._log(f"Extracted {len(elements)} elements filtering for {class_name}")
        return elements

    def _extract_contents(self, elements):
        contents = {}
        for elem in elements:
            contents[elem.text] = 'https://issuu.com' + elem.get('href')
        self._log(f"Extracted {len(contents)} elements from {len(elements)} elements")
        return contents

    def fetch_filter_and_extract_contents_from_issuu_page(self, issuu_page_url):
        web_page = self._fetch_html_web_page(issuu_page_url)
        publication_class = 'PublicationCard__publication-card__card-link__hUKEG__0-0-3094'
        filtered_elements = self._filter_elements_by_class(web_page, publication_class)
        contents = self._extract_contents(filtered_elements)
        return contents

    def fetch_filter_and_extract_pagination_data_from_issuu_page(self, issuu_page_url):
        pagination_class = 'Pagination__pagination__inner__iHwTs__0-0-3094'
        web_page = self._fetch_html_web_page(issuu_page_url)
        elements = self._filter_elements_by_class(web_page, pagination_class)
        return elements