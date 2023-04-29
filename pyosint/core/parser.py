import requests
from bs4 import BeautifulSoup

ua = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
}


class Parser:
    def __init__(self, url: str, request_type: str, data: dict = None):
        self.url: str = url
        self.request_type: str = request_type
        self.data: dict = data

        self.soup = None

    def get_request(self):
        return requests.get(self.url, data=self.data, headers=ua)

    def post_request(self):
        return requests.post(self.url, data=self.data)

    def make_request(self):
        if self.request_type == 'get':
            return self.get_request()
        elif self.request_type == 'post':
            return self.post_request()

    def get_content(self):
        return self.make_request().content

    def get_status_code(self):
        return self.make_request().status_code

    def get_soup(self):
        if not self.soup:
            self.soup = BeautifulSoup(self.get_content(), features="html.parser")
        return self.soup

    def get_all_elements(self, element: str, attributes: dict = None, parent_element=None) -> list|None:
        parent_element = parent_element if parent_element else self.get_soup()
        try:
            return parent_element.find_all(element, attributes)
        except AttributeError:
            return None

    def get_all_attrs_values(
            self, attr_key: str, attributes: dict = None, elements_list: list = None, html_element: str = None
    ) -> list:
        elements_list = elements_list if elements_list else self.get_all_elements(html_element, attributes)
        return [self.get_attribute(el, attr_key) for el in elements_list]

    @staticmethod
    def get_element_text(element):
        if isinstance(element, list):
            return [el.get_text(strip=True, separator=' ').replace("\xa0", ' ') for el in element]
        else:
            return element.get_text(strip=True, separator=' ').replace("\xa0", ' ')

    @staticmethod
    def get_attribute(parent_object, children_object):
        return parent_object.get(children_object)
