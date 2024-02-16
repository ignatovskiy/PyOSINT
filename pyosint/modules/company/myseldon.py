from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://basis.myseldon.com"


class Myseldon(Company):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.make_request('get', url).json()['response']['items']
        return orgs_dict

    def format_org_dict(self, org: dict):
        return self.flatten_card_data(org)

    def get_search_results(self):
        return self.get_lists_of_orgs()

    def get_complex_data(self):
        return self.flatten_card_data(self.get_search_results())

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/en/home/searchdata/?searchString={input_data}"

    def get_company_info(self, url):
        pass


def main():
    handle_cmd_args_module(Myseldon)


if __name__ == "__main__":
    main()
