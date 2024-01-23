from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://api.facha.dev"


class Facha(Web):
    types = ['ip']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_request_content(self.make_request('get', url), return_json=True)

    def get_search_url(self, input_data):
        return f"{URL}/v1/ip/{input_data}"

    def get_complex_data(self):
        complex_data = self.get_parsed_object(self.get_search_url(self.input_data))
        return complex_data


def main():
    handle_cmd_args_module(Facha)


if __name__ == "__main__":
    main()
