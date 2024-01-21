from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://www.clearwebstats.com"


class ClearWebStats(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/task.php?q={input_data}&t=auto"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        tables = self.get_all_elements_from_parent(parsed, 'table')
        complex_data = {}
        indexes = [0, 1, 2, 3, 4, 5, 6, 9, 10]

        for index in indexes:
            temp_trs = self.get_all_elements_from_parent(tables[index], 'tr')
            temp_table = self.parse_table(temp_trs)
            complex_data.update(temp_table)

        useless_values = ["Not Applicable", '']
        complex_data = {key: value for key, value in complex_data.items() if
                        isinstance(value, list) or value not in useless_values}
        return complex_data


def main():
    handle_cmd_args_module(ClearWebStats)


if __name__ == "__main__":
    main()
