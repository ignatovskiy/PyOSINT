from pyosint.core.utils import *
import re


URL = "https://w3techs.com/sites/info"


class W3techs:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/{input_data}"

    def get_site_info(self):
        url = self.get_search_url(self.input_data)
        parsed = self.get_parsed_object(url)
        table = get_all_elements_from_parent(parsed, 'td', attributes={'class': 'tech_main'})[0]
        ps = get_all_elements_from_parent(table, 'p',
                                          attributes={'class': [re.compile(r'\bsi_h\b'), re.compile(r'\bsi_tech\b')]})
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
        if techs_dict.get('No title declaration'):
            techs_dict.pop('No title declaration')
        return techs_dict


def main():
    pass


if __name__ == "__main__":
    main()
