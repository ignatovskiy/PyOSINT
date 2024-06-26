from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://ip2geolocation.com"


class Ip2Location(Web):
    types = ['ip']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/?ip={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        tables = self.get_all_elements_from_parent(parsed,'table')[1:3]
        complex_data = []
        for table in tables:
            trs = self.get_all_elements_from_parent(table, 'tr')
            temp_table = self.parse_table(trs)
            complex_data.append(temp_table)
        return complex_data


def main():
    handle_cmd_args_module(Ip2Location)


if __name__ == "__main__":
    main()
