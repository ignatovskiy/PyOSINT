import requests
from bs4 import BeautifulSoup


ua = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"}


class Parser:
    def __init__(self, url: str, request_type: str, data: dict = None):
        self.url: str = url
        self.request_type: str = request_type
        self.data: dict = data
        self.requests = {
            'get': self.get_request(),
            'post': self.post_request()
        }

    def get_request(self):
        return requests.get(self.url, data=self.data, headers=ua)

    def post_request(self):
        return requests.post(self.url, data=self.data)

    def make_request(self):
        return self.requests[self.request_type]

    def get_content(self):
        return self.make_request().content

    def get_status_code(self):
        return self.make_request().status_code

    def get_soup(self):
        return BeautifulSoup(self.get_content(), features="html.parser")

    def get_all_elements(self, element: str, attributes: dict = None) -> list:
        return self.get_soup().find_all(element, attributes)

    def get_all_attrs_values(self, html_element: str, attr_key: str, attributes: dict = None) -> list:
        return [el.get(attr_key) for el in self.get_all_elements(html_element, attributes)]
