from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://well-known.dev"


class WellKnown(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data, page):
        return f"{URL}/?q={input_data}&page={page}"

    def get_complex_data(self):
        data_list = []

        def process_iteration(index):
            parsed = self.get_parsed_object(self.get_search_url(self.input_data, index))
            table = self.get_all_elements_from_parent(parsed, 'table', {"class": "responsive grid"})[0]
            trs = self.get_all_elements_from_parent(table, 'tr')
            ths = self.get_all_elements_from_parent(table, 'th')
            table_data = self.parse_table(trs, headers=ths, first_row_index=1)
            if isinstance(table_data, dict):
                table_data = [table_data]
            data_list.extend(table_data)
            disabled_next_page = self.get_all_elements_from_parent(parsed, "a", {"class": "disabled"})
            if disabled_next_page and "Next" in self.parse_strings_list(disabled_next_page):
                return True

        self.process_requests_concurrently(process_iteration, while_mode=True)
        return data_list


def main():
    handle_cmd_args_module(WellKnown)


if __name__ == "__main__":
    main()
