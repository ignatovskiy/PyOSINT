from pyosint.core.utils import *


URL = ""


class TemplateCompany:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = make_request('get', url).json()
        return orgs_dict

    def get_search_results(self):
        results = []
        for org in self.get_lists_of_orgs():
            temp_dict = org
            results.append(temp_dict)
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
        return f"{URL}/{input_data}"

    def get_company_info(self, url):
        info_dict = dict()
        return info_dict


def main():
    print(TemplateCompany("Example").get_company_info("example.site"))


if __name__ == "__main__":
    main()
