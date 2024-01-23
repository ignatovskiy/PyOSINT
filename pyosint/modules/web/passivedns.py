from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://api.mnemonic.no"


class PassiveDNS(Web):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        json_ = {
            "offset": 0,
            "limit": 100,
            "query": self.input_data,
            "tlp": [],
            "aggregateResult": True,
            "includeAnonymousResults": True,
            "rrClass": [],
            "rrType": []
        }
        return self.get_request_content(self.make_request('post', url, json_=json_), return_json=True)

    def get_search_url(self, input_data):
        return f"{URL}/pdns/v3/search"

    def get_complex_data(self):
        complex_data = self.get_parsed_object(self.get_search_url(self.input_data))['data']
        return complex_data


def main():
    handle_cmd_args_module(PassiveDNS)


if __name__ == "__main__":
    main()
