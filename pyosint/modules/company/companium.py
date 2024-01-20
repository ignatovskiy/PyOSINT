from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://companium.ru"


class Companium(Company):
    types = ["id", "company"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.make_request('get', url).json()
        return orgs_dict

    def get_search_results(self):
        results = []
        for org in self.get_lists_of_orgs():
            temp_dict = org
            temp_dict['info'] = self.get_soup_from_raw(temp_dict['content'])
            temp_dict.pop('content')
            temp_id = self.get_all_elements_from_parent(temp_dict['info'], 'a')[0].get('href')[4:].split('-')[0]
            temp_dict['url'] = f"{URL}/id/{temp_id}"
            temp_dict['info'] = self.parse_strings_list(temp_dict['info'])
            results.append(temp_dict)
        return results

    def get_complex_data(self):
        search_results = self.get_search_results()
        complex_data = {}

        for result in search_results:
            company_name = result['info'][0]
            company_ogrn = result['ogrn']
            complex_data[company_name] = {}
            complex_data[company_name][company_ogrn] = self.get_company_info(result['url'])

        return complex_data

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/search/tips?query={input_data}"

    def get_brief_info(self, url):
        parsed = self.get_parsed_object(url)
        brief_info_dict = dict()
        brief_info_div = self.get_all_elements_from_parent(parsed, 'div',
                                                           attributes={'class': 'col-12 col-xl-6 border-xl-start'})[0]
        brief_info_subdivs = self.get_all_elements_from_parent(brief_info_div, 'div', recursive=False)
        temp_text_list = self.parse_strings_list(brief_info_subdivs)
        for temp_text_el in temp_text_list:
            temp_title = temp_text_el[0]
            temp_text = temp_text_el[1:]
            if len(temp_text) == 1:
                temp_text = temp_text[0]
            brief_info_dict[temp_title] = temp_text
        return brief_info_dict

    def get_contact_info(self, url):
        parsed = self.get_parsed_object(url)
        parsed_text = self.parse_strings_list(
            self.get_all_elements_from_parent(parsed, 'div', {'class': "container-xl mt-4 mb-5"}))
        return parsed_text[:-3]

    def get_company_sphere_info(self, url, key, page=None, headers=None, params=None):
        info_dict = {key: {}}

        if page is None:
            page = key

        parsing_urls = [url + f"/{page}?type={param}" for param in params] if params else [url + f"/{page}"]
        params = params if params else [None] * len(parsing_urls)
        for parsing_url, param in zip(parsing_urls, params):
            parsed = self.get_parsed_object(parsing_url)
            tables = self.get_all_elements_from_parent(parsed, 'table')
            headers = headers if headers else [None] * len(tables)
            table = []

            if len(tables) != 0:
                for row_table in tables:
                    trs = self.get_all_elements_from_parent(row_table, 'tr')
                    ths = self.get_all_elements_from_parent(row_table, headers) if any(headers) else None
                    table.append(self.parse_table(trs, headers=ths, collection_type='dict'))

            table = self.flatten_card_data(table)
            if any(params):
                info_dict[key][param] = table
            else:
                info_dict[key] = table
        return info_dict

    def get_company_info(self, url):
        info_dict = dict()
        info_dict["info"] = self.get_brief_info(url)
        info_dict["contact"] = self.get_contact_info(url + "/contacts")

        info_dict.update(self.get_company_sphere_info(url, 'ids', page='details', headers='strong'))
        info_dict.update(self.get_company_sphere_info(
            url, 'connections', params=["management", "founders", "managed", "founded", "predecessors", "successors"]))

        simple_tables = ["accounting", "purchases",
                         "inspections", "legal-cases", "enforcements", "fedresurs", "licenses", "branches", "activity"]
        for simple_table in simple_tables:
            info_dict.update(self.get_company_sphere_info(url, simple_table))
        return info_dict


def main():
    handle_cmd_args_module(Companium)


if __name__ == "__main__":
    main()
