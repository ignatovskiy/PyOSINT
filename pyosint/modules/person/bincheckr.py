from pyosint.core.categories.person import Person
from pyosint.core.cmd import handle_cmd_args_module


URL = "http://bincheckr.com"


class BinCheckr(Person):
    types = ['id']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('post', url)))

    def get_search_url(self, input_data):
        return f"{URL}/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        tables = self.get_all_elements_from_parent(parsed, 'table')
        complex_data = []
        for table in tables:
            ths = self.get_all_elements_from_parent(table, 'th')
            trs = self.parse_strings_list(self.get_all_elements_from_parent(table, 'td')[1:])
            if isinstance(trs[-1], list):
                trs = [el if isinstance(el, str) else " ".join(el) for el in trs]
            temp_table = self.parse_table(trs, headers=ths, tds_ready=True, first_row_index=1)
            complex_data.append(temp_table)
        return complex_data


def main():
    handle_cmd_args_module(BinCheckr)


if __name__ == "__main__":
    main()
