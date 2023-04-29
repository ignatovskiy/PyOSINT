from pyosint.core.parser import Parser


URL = "https://www.tinkoff.ru/api/common/dadata/suggestions/api/4_1/rs/suggest/party?appName=company-pages"
COMPANY_URL = "https://www.tinkoff.ru/business/contractor/legal"


class Tinkoff:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.get_parsed_object(url).get_request().json()
        return orgs_dict

    def remove_null_dict_values(self, org):
        for key, value in list(org.items()):
            if isinstance(value, dict):
                self.remove_null_dict_values(value)
                if not value:
                    del org[key]
            elif value is None:
                del org[key]
        return org

    def format_org_dict(self, org: dict):
        org.pop('unrestricted_value')
        org['data']['address'].pop('data')
        org['url'] = f"{COMPANY_URL}/{org['data']['ogrn']}/"
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

    @staticmethod
    def get_parsed_object(url):
        return Parser(url, 'get')

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
            divs_list = parsed.get_all_elements('div', {'class': 'anc1Re'})
            if divs_list:
                for div in divs_list:
                    temp_title = " ".join(parsed.get_element_text(parsed.get_all_elements('h2', parent_element=div)))
                    temp_text = " ".join(parsed.get_element_text(parsed.get_all_elements('p', parent_element=div)))
                    if not info_dict.get(temp_title):
                        info_dict[temp_title] = [temp_text]
                    else:
                        info_dict[temp_title].append(temp_text)
            else:
                break
        return {"changes": info_dict}


def main():
    a = Tinkoff('Рг-Групп').get_company_info('https://www.tinkoff.ru/business/contractor/legal/1107847232063/')
    print(a)


if __name__ == "__main__":
    main()
