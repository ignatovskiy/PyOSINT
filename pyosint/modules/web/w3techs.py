import re

from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://w3techs.com"


class W3techs(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/sites/info/{input_data}"

    def get_complex_data(self):
        url = self.get_search_url(self.input_data)
        parsed = self.get_parsed_object(url)
        table = self.get_all_elements_from_parent(parsed, 'td', attributes={'class': 'tech_main'})[0]
        ps = self.get_all_elements_from_parent(table, 'p',
                                               attributes={
                                                   'class': [re.compile(r'\bsi_h\b'), re.compile(r'\bsi_tech\b')]})
        ps_text = [el for el in ps if el.a and el.a.text]
        complex_data = {}
        temp_key = None
        for text in ps_text:
            if text.attrs['class'][0] == 'si_h':
                temp_key = text.a.text
                complex_data[temp_key] = []
            if text.attrs['class'][0] == 'si_tech':
                complex_data[temp_key].append(text.a.text)
        for key in complex_data:
            if len(complex_data[key]) == 1:
                complex_data[key] = complex_data[key][0]
        if complex_data.get('No title declaration'):
            complex_data.pop('No title declaration')
        return complex_data


def main():
    handle_cmd_args_module(W3techs)


if __name__ == "__main__":
    main()
