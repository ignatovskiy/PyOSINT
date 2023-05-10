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
        tables = get_all_elements_from_parent(parsed, 'table')
        based_data = dict()
        headers = get_element_text(get_all_elements_from_parent(parsed, 'p',
                                                                {'style': "color: #ddd; font-family: 'Courier New', Courier, monospace; text-align: left;"}))
        for header, table in zip(headers, tables):
            trs = get_all_elements_from_parent(table, 'tr')
            parsed_table = parse_table(trs, parsed, do_list=True)
            header = header.split(" **")[0]
            based_data.update({header: parsed_table})
        return based_data


def main():
    print(DNSDumpster("wotblitz.com").get_site_info())


if __name__ == "__main__":
    main()
