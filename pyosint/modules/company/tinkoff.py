from pyosint.core.parser import Parser
from pyosint.core.utils import *


URL = "https://www.tinkoff.ru/api/common/dadata/suggestions/api/4_1/rs/suggest/party?appName=company-pages"
COMPANY_URL = "https://www.tinkoff.ru/business/contractor/legal"


class Tinkoff:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = make_request('get', url).json()
        return orgs_dict

    @staticmethod
    def format_org_dict(org: dict):
        org.pop('unrestricted_value')
        org['data']['address'].pop('data')
        org['url'] = f"{COMPANY_URL}/{org['data']['ogrn']}/"
        return remove_null_dict_values(org)

    def get_search_results(self):
        results = []
        for org in self.get_lists_of_orgs()['suggestions']:
            results.append(self.format_org_dict(org))
        return results

    def get_complex_data(self):
        search_results = self.get_search_results()
        complex_data = []

        for result in search_results:
            complex_data.append(self.get_company_info(result['url']))

        return complex_data

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}&count=20&query={input_data}"

    def get_company_info(self, url):
        info_dict = {}
        counter = 0
        while True:
            counter += 1
            temp_url = f"{url}/history/{counter}/"
            parsed = self.get_parsed_object(temp_url)
            divs_list = get_all_elements_from_parent(parsed, 'div', attributes={'class': 'anc1Re'})
            if divs_list:
                for div in divs_list:
                    temp_title = " ".join(get_element_text(get_all_elements_from_parent(div, 'h2')))
                    temp_text = " ".join(get_element_text(get_all_elements_from_parent(div, 'p')))
                    if not info_dict.get(temp_title):
                        info_dict[temp_title] = [temp_text]
                    else:
                        info_dict[temp_title].append(temp_text)
            else:
                break
        return {"changes": info_dict}


def main():
    pass


if __name__ == "__main__":
    main()
