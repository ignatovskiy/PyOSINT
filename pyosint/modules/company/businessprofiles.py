from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://businessprofiles.com"


class BusinessProfiles(Company):
    types = ['company']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        raw_page = self.get_parsed_object(url)
        div_results = self.get_all_elements_from_parent(raw_page,
                                                        'div',
                                                        {"class": "results_display"})[0]
        links = self.get_all_elements_from_parent(div_results, 'a')
        list_of_orgs = {}
        for link in links:
            url = f"{URL}{link.get('href')}"
            list_of_orgs[url] = self.parse_strings_list(link)
        return list_of_orgs

    def format_org_dict(self, org: dict):
        return self.flatten_card_data(org)

    def get_search_results(self):
        return self.get_lists_of_orgs()

    def get_complex_data(self):
        return [self.get_company_info(result) for result in self.get_search_results()]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/companies?jurisdiction=&q={input_data}"

    def get_company_info(self, url):
        def separate_odd_even_indices(input_list):
            even_indices = [element for index, element in enumerate(input_list) if index % 2 == 0]
            odd_indices = [element for index, element in enumerate(input_list) if index % 2 != 0]

            return even_indices, odd_indices

        parsed = self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))
        title = self.parse_strings_list(self.get_all_elements_from_parent(parsed, 'h1')[0])

        div_details = self.get_all_elements_from_parent(parsed,
                                                        'div',
                                                        {"class": "details_content clearfix"})
        if len(div_details) >= 1:
            div_details = self.parse_strings_list(div_details[0])

        div_addrs = self.get_all_elements_from_parent(parsed,
                                                      'div',
                                                      {"class": "location_content clearfix"})
        if len(div_addrs) >= 1:
            div_addrs = self.parse_strings_list(div_addrs[0])

        div_officers = self.get_all_elements_from_parent(parsed,
                                                         'div',
                                                         {"class": "officers_content clearfix"})
        if len(div_officers) >= 1:
            strings = self.parse_strings_list(div_officers[0])
            headers, values = separate_odd_even_indices(strings)
            div_officers = self.parse_table(trs=values, tds_ready=True, first_row_index=1, headers=headers)

        return {title: {'details': div_details, 'address': div_addrs, 'rulers': div_officers}}


def main():
    handle_cmd_args_module(BusinessProfiles)


if __name__ == "__main__":
    main()
