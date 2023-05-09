from pyosint.core.parser import Parser
from pyosint.core.utils import *
import re


URL = "https://w3techs.com/sites/info"


class W3techs:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return Parser(url, 'get')

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/{input_data}"

    def get_site_info(self):
        url = self.get_search_url(self.input_data)
        parsed = self.get_parsed_object(url)
        table = parsed.get_all_elements('td', {'class': 'tech_main'})[0]
        ps = parsed.get_all_elements('p', {'class': [re.compile(r'\bsi_h\b'), re.compile(r'\bsi_tech\b')]},
                                     parent_element=table)
        ps_text = [el for el in ps if el.a.text]
        techs_dict = dict()
        temp_key = None
        for text in ps_text:
            if text.attrs['class'][0] == 'si_h':
                temp_key = text.a.text
                techs_dict[temp_key] = []
            if text.attrs['class'][0] == 'si_tech':
                techs_dict[temp_key].append(text.a.text)
        for key in techs_dict:
            if len(techs_dict[key]) == 1:
                techs_dict[key] = techs_dict[key][0]
        techs_dict.pop('No title declaration')
        return techs_dict


def main():
    test = W3techs("microsoft.com").get_site_info()
    print(test)


if __name__ == "__main__":
    main()
