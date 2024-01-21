from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://www.geodatatool.com"


class GeoDataTool(Web):
    types = ["ip", "hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/en/?ip={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        div = self.get_all_elements_from_parent(parsed, 'div', {'class': 'sidebar-data hidden-xs hidden-sm'})[0]
        divs = self.get_all_elements_from_parent(div, 'div', {'class': 'data-item'})
        complex_data = self.flatten_card_data(self.get_cells_data(tds=self.parse_strings_list(divs),
                                                                  list_of_lists=True))
        return complex_data


def main():
    handle_cmd_args_module(GeoDataTool)


if __name__ == "__main__":
    main()
