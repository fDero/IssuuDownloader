import json


def scrape_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }


def download_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "image/jpg",
        "Accept-Language": "en-US,en;q=0.5"
    }


def download_init_headers(payload):
    payload_json = json.dumps(payload)
    content_length = len(payload_json.encode('utf-8'))
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "application/json",
        "Accept-Encoding": "utf8",
        "Content-Length": str(content_length),
        "Content-Type": "application/json",
        "Custom-Request-Id": "44AA3F37-FBED-4B77-BE51-5CFC2FED5869",
        "Origin": "https://issuudownload.com",
        "Priority": "u=1, i",
        "Refer": "https://issuudownload.com/",
        "Scope": "issuu",
        "Sec-Ch-ua": 'Google Chrome;v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-Ch-ua-Mobile": "?0",
        "Sec-Ch-ua-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }


def download_check_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "application/json",
        "Accept-Encoding": "utf8",
        "Content-Type": "application/json",
        "Custom-Request-Id": "44AA3F37-FBED-4B77-BE51-5CFC2FED5869",
        "Origin": "https://issuudownload.com",
        "Priority": "u=1, i",
        "Refer": "https://issuudownload.com/",
        "Scope": "issuu",
        "Sec-Ch-ua": 'Google Chrome;v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-Ch-ua-Mobile": "?0",
        "Sec-Ch-ua-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }