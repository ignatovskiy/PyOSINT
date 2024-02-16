from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://orbisdirectory-r1.bvdinfo.com"


class OrbisDirectory(Company):
    types = ['company']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.get_soup_from_raw(
            self.get_request_content(self.make_request('post',
                                                       url,
                                                       new_headers={'Content-Type':
                                                                    'application/x-www-form-urlencoded'})))
        lis = self.get_all_elements_from_parent(orgs_dict, 'li')
        ps = [self.parse_strings_list(self.get_all_elements_from_parent(li, 'p')) + [f"{URL}{li.a.get('href')}"]
              for li in lis]
        list_of_orgs = []

        for p in ps:
            temp_dict = dict()
            temp_dict['Company'] = p[0]
            temp_dict['Info'] = p[1:-1]
            temp_dict['URL'] = p[-1]
            list_of_orgs.append(temp_dict)

        return list_of_orgs

    def format_org_dict(self, org: dict):
        return self.flatten_card_data(org)

    def get_search_results(self):
        return [self.format_org_dict(org) for org in self.get_lists_of_orgs()]

    def get_complex_data(self):
        return [self.get_company_info(result['URL']) for result in self.get_search_results()]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        args = f"IsXMLHttpRequest=true&term={input_data}&token=1"
        return f"{URL}/version-20231205-1-1/OrbisDirectory/1/Companies/Search/QuickSearch?{args}"

    def get_company_info(self, url):
        parsed = self.get_parsed_object(url)
        info_list = []
        div = self.get_all_elements_from_parent(parsed, 'div', {"class": "onePage t6 g1"})[0]
        table_data = self.get_all_elements_from_parent(div, 'table')[0]
        last_div = self.get_all_elements_from_parent(div, 'div', {"class": "report-box t6"})[0]
        info_list.append(self.parse_strings_list(last_div)[0])
        info_list.extend(self.parse_strings_list(table_data))
        return info_list


def main():
    handle_cmd_args_module(OrbisDirectory)


if __name__ == "__main__":
    main()
