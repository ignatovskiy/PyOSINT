from pyosint.core.parser import Parser
from pyosint.core.utils import *


URL = "https://dnsdumpster.com/"


class DNSDumpster:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/?url={input_data}"

    def get_site_info(self):
        parsed = get_csrf_site_content(URL, {'targetip': self.input_data, 'user': 'free'})
        table_data = get_table_dict(parsed)
        return table_data


def main():
    pass


if __name__ == "__main__":
    main()
