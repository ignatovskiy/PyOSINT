from pyosint.core.templates.company import Company


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
        return self.remove_null_dict_values(org)

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

    def get_company_info(self, url):
        info_dict = {}
        counter = 0
        while True:
            counter += 1
            temp_url = f"{url}/history/{counter}/"
            parsed = self.get_parsed_object(temp_url)
            divs_list = self.get_all_elements_from_parent(parsed,
                                                          'div',
                                                          attributes={'automation-id': 'history-wrapper'})[0]
            subdivs_list = self.get_all_elements_from_parent(divs_list, 'div')
            if subdivs_list:
                for div in subdivs_list:
                    temp_title = " ".join(self.get_element_text(self.get_all_elements_from_parent(div, 'h2')))
                    temp_text = " ".join(self.get_element_text(self.get_all_elements_from_parent(div, 'p')))
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
