from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://mac.lc"


class MacLc(Web):
    types = ["id"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/address/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        table = self.get_all_elements_from_parent(parsed, 'table')[1]
        trs = self.get_all_elements_from_parent(table, 'tr')
        ths = self.get_all_elements_from_parent(table, 'th')
        table_data = self.parse_table(trs, headers=ths, first_row_index=1)
        return table_data


def main():
    handle_cmd_args_module(MacLc)


if __name__ == "__main__":
    main()
