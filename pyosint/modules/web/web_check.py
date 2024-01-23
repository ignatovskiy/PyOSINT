from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://web-check.as93.net"


class WebCheck(Web):
    types = ['hostname']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_request_content(self.make_request('get', url), return_json=True)

    def get_search_url(self, input_data, mode):
        return f"{URL}/.netlify/functions/{mode}?url={input_data}"

    def get_complex_data(self):
        complex_data = {}
        modes = ["whois", "cookies", "headers", "dns", "http-security",
                 "social-tags", "threats", "mail-config"]

        def process_mode(mode):
            parsed = self.get_parsed_object(self.get_search_url(self.input_data, mode))
            if parsed:
                if mode == 'whois':
                    parsed = parsed['whoisData']
                complex_data[mode] = self.flatten_card_data(parsed)

        self.process_requests_concurrently(process_mode, reqs=modes)
        return complex_data


def main():
    handle_cmd_args_module(WebCheck)


if __name__ == "__main__":
    main()
