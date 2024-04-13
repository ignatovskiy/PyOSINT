from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://whoisrequest.com"


class WhoisRequest(Web):
    types = ['hostname']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/whois/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        pre = self.get_all_elements_from_parent(parsed, 'pre')[0]
        pre_text = self.parse_strings_list(pre)
        text = [el.split(' ') for el in pre_text]
        complex_data = [sublist
                        for list_ in self.flatten_card_data(text)
                        for sublist in list_
                        if not isinstance(sublist, dict)]
        return complex_data


def main():
    handle_cmd_args_module(WhoisRequest)  # TODO fix


if __name__ == "__main__":
    main()
