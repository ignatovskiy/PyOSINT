from pyosint.core.utils import *


URL = "https://crt.sh/?q="


class Crt:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url, use_default_headers=False)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}{input_data}"

    def get_site_info(self):
        url = self.get_search_url(self.input_data)
        parsed = self.get_parsed_object(url)
        table = get_all_elements_from_parent(parsed, 'table')[-1]
        trs = get_all_elements_from_parent(table, 'tr')
        parsed_table = parse_table(trs, parsed)
        return parsed_table


def main():
    pass


if __name__ == "__main__":
    main()
