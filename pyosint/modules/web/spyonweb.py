from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://spyonweb.com"


class SpyOnWeb(Web):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        divs = self.get_all_elements_from_parent(parsed, 'div', {"class": "links"})
        headers = self.parse_strings_list(self.get_all_elements_from_parent(parsed,
                                                                            'h3',
                                                                            {"class": "panel-title"}))
        headers = [el[0] for el in headers]
        complex_data = {}
        for div, header in zip(divs, headers):
            temp_links = self.parse_strings_list(div)
            complex_data[header] = temp_links
        return complex_data


def main():
    handle_cmd_args_module(SpyOnWeb)


if __name__ == "__main__":
    main()
