from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module


URL = ""


class CompanyModule(Company):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.make_request('get', url).json()
        return orgs_dict

    def format_org_dict(self, org: dict):
        return self.flatten_card_data(org)

    def get_search_results(self):
        return [self.format_org_dict(org) for org in self.get_lists_of_orgs()]

    def get_complex_data(self):
        return [self.get_company_info(result['url']) for result in self.get_search_results()]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/{input_data}"

    def get_company_info(self, url):
        info_dict = {}
        parsed = self.get_parsed_object(url)
        info_dict = parsed
        return info_dict


def main():
    handle_cmd_args_module(CompanyModule)


if __name__ == "__main__":
    main()
