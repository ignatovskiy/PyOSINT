from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.opensanctions.org"


class OpenSanctions(Company):
    types = ['company']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))
        list_of_orgs = []
        lis = self.get_all_elements_from_parent(orgs_dict, 'li', {"class": "Search_resultItem__RNdvE"})
        for li in lis:
            temp_dict = dict()
            temp_link = li.a
            temp_dict["URL"] = f"{URL}{temp_link.get('href')}"
            temp_dict["Company"] = self.parse_strings_list(temp_link)
            temp_data = self.flatten_card_data(
                self.parse_strings_list(self.get_all_elements_from_parent(li, 'p')))
            temp_dict["Country"] = temp_data[-1]
            temp_dict["Type"] = temp_data[0]
            temp_dict["Data"] = temp_data[1:-1]
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
        return f"{URL}/search/?q={input_data}"

    def get_company_info(self, url):
        info_dict = []

        parsed = self.get_parsed_object(url)
        div = self.get_all_elements_from_parent(parsed, 'div', {"class": "order-2 col-md-9"})[0]
        tables = self.get_all_elements_from_parent(div, 'table')

        for table in tables:
            trs = []
            for tr in self.get_all_elements_from_parent(table, 'tr'):
                temp_trs = self.parse_strings_list(tr)
                trs.append(temp_trs[:-1])
            temp_table = self.flatten_card_data(self.get_cells_data(tds=trs, list_of_lists=True))
            info_dict.append(temp_table)

        return self.flatten_card_data(info_dict)


def main():
    handle_cmd_args_module(OpenSanctions)


if __name__ == "__main__":
    main()
