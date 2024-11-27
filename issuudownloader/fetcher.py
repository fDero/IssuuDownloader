from bs4 import BeautifulSoup
from .utils import *
import requests


class IssuuFetcher:
    def __init__(self, logging_callback=None):
        if logging_callback is None:
            logging_callback = print
        self.logging_callback = logging_callback

    def fetch_html_web_page(self, url):
        response = requests.get(url, headers=scrape_headers())
        response.raise_for_status()
        self.logging_callback(f"Successfully fetched from {url}")
        return response.content

    def filter_elements_by_class(self, web_page, class_name):
        soup = BeautifulSoup(web_page, features='html.parser')
        elements = soup.find_all(class_=class_name)
        self.logging_callback(f"Extracted {len(elements)} elements filtering for {class_name}")
        return elements

    def extract_contents(self, elements):
        contents = {}
        for elem in elements:
            contents[elem.text] = 'https://issuu.com' + elem.get('href')
        self.logging_callback(f"Extracted {len(contents)} elements from {len(elements)} elements")
        return contents

    def fetch_filter_and_extract_contents_from_issuu_page(self, issuu_page_url):
        web_page = self.fetch_html_web_page(issuu_page_url)
        filtered_elements = self.filter_elements_by_class(web_page, class_name='PublicationCard__publication-card__card-link__hUKEG__0-0-3094')
        contents = self.extract_contents(filtered_elements)
        return contents