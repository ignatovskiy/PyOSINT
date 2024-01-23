from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "websiteoutlook.com"


class WebsiteOutlook(Web):
    types = ['hostname']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"https://{input_data}.{URL}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        tables = self.get_all_elements_from_parent(parsed, 'table')
        complex_data = []
        for table in tables:
            trs = self.get_all_elements_from_parent(table, 'tr')
            parsed_table = self.parse_table(trs)
            if isinstance(parsed_table, list):
                parsed_table = self.flatten_card_data(parsed_table[:-1])
            complex_data.append(parsed_table)
        return complex_data


def main():
    handle_cmd_args_module(WebsiteOutlook)


if __name__ == "__main__":
    main()
