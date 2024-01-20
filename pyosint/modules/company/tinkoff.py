from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.tinkoff.ru"


class Tinkoff(Company):
    types = ["company"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.make_request('get', url).json()
        return orgs_dict

    def format_org_dict(self, org: dict):
        org.pop('unrestricted_value')
        org['data']['address'].pop('data')
        org['url'] = f"{URL}/business/contractor/legal/{org['data']['ogrn']}/"
        return self.flatten_card_data(org)

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

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        uri = "api/common/dadata/suggestions/api/4_1/rs/suggest/party?appName=company-pages&count=20"
        return f"{URL}/{uri}&query={input_data}"

    def get_company_history(self, url):
        history_dict = {}
        counter = 0
        while True:
            counter += 1
            temp_url = f"{url}/{counter}/"
            parsed = self.get_parsed_object(temp_url)
            divs_list = self.get_all_elements_from_parent(parsed,
                                                          'div',
                                                          attributes={'automation-id': 'history-wrapper'})[0]
            subdivs_list = self.get_all_elements_from_parent(divs_list, 'div')
            if subdivs_list:
                for div in subdivs_list:
                    temp_title = self.parse_strings_list(self.get_all_elements_from_parent(div, 'h2'))
                    temp_text = self.parse_strings_list(self.get_all_elements_from_parent(div, 'p'))
                    if not history_dict.get(temp_title):
                        history_dict[temp_title] = [temp_text]
                    else:
                        history_dict[temp_title].append(temp_text)
            else:
                break
        return history_dict

    def get_company_finance(self, url):
        finance_dict = []
        parsed = self.get_parsed_object(url)
        tables = self.get_all_elements_from_parent(parsed, 'table')
        for table in tables:
            temp_trs = self.get_all_elements_from_parent(table, 'tr')
            temp_table = self.parse_table(temp_trs, collection_type='dict')
            finance_dict.append(temp_table)
        return self.flatten_card_data(finance_dict)

    def get_company_info(self, url):
        info_dict = dict()
        info_dict['changes'] = self.get_company_history(f"{url}/history")
        info_dict['finance'] = self.get_company_finance(f"{url}/financial-statements")
        return info_dict


def main():
    handle_cmd_args_module(Tinkoff)


if __name__ == "__main__":
    main()
