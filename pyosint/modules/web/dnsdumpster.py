from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://dnsdumpster.com/"


class DNSDumpster(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/?url={input_data}"

    def get_complex_data(self):
        parsed = self.get_csrf_site_content(URL, URL, {'targetip': self.input_data, 'user': 'free'})
        tables = self.get_all_elements_from_parent(parsed, 'table')
        complex_data = {}
        style = "color: #ddd; font-family: 'Courier New', Courier, monospace; text-align: left;"
        headers = self.parse_strings_list(
            self.get_all_elements_from_parent(parsed,
                                              'p',
                                              {'style': style}))
        for header, table in zip(headers, tables):
            trs = self.get_all_elements_from_parent(table, 'tr')
            parsed_table = self.parse_table(trs)
            header = header[0] if isinstance(header, list) else header
            complex_data.update({header: parsed_table})
        return complex_data


def main():
    handle_cmd_args_module(DNSDumpster)


if __name__ == "__main__":
    main()
