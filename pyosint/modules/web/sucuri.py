from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://sitecheck.sucuri.net"


class Sucuri(Web):
    types = ['hostname']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.make_request('get', url).json()

    def get_search_url(self, input_data):
        return f"{URL}/api/v3/?scan={input_data}"

    def get_complex_data(self):
        complex_data = self.get_parsed_object(self.get_search_url(self.input_data))
        return self.flatten_card_data(complex_data)


def main():
    handle_cmd_args_module(Sucuri)


if __name__ == "__main__":
    main()
