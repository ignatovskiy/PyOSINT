from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://dnsspy.io"


class DnsSpy(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/scan/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        h1_list = self.parse_strings_list(self.get_all_elements_from_parent(parsed, 'h1')[1:])
        tables = self.get_all_elements_from_parent(parsed, 'table')
        complex_data = {}
        for table, h1 in zip(tables, h1_list):
            trs = self.get_all_elements_from_parent(table, 'tr')
            ths = self.get_all_elements_from_parent(table, 'th')
            parsed_table = self.parse_table(trs, headers=ths, first_row_index=1)
            complex_data[h1] = parsed_table
        return complex_data


def main():
    handle_cmd_args_module(DnsSpy)


if __name__ == "__main__":
    main()
