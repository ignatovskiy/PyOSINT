from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://check-host.net"


class CheckHost(Web):
    types = ['hostname', 'ip']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_request_content(self.make_request('get',
                                                          url,
                                                          new_headers={"Accept": "application/json"}), return_json=True)

    def get_search_url(self, input_data):
        return f"{URL}/check-tcp?host={input_data}&max_nodes=20"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        result_url = f"{URL}/check-result/{parsed['request_id']}"
        complex_data = self.get_request_content(self.make_request('get',
                                                                  result_url,
                                                                  new_headers={"Accept": "application/json"},
                                                                  pre_sleep=3),
                                                return_json=True)
        return complex_data


def main():
    handle_cmd_args_module(CheckHost)


if __name__ == "__main__":
    main()
