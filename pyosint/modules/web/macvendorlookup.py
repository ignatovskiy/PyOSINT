from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.macvendorlookup.com"


class MacVendorLookup(Web):
    types = ["id"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.make_request('get', url).json()

    def get_search_url(self, input_data):
        return f"{URL}/oui.php?mac={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))[0]
        return parsed


def main():
    handle_cmd_args_module(MacVendorLookup)


if __name__ == "__main__":
    main()
