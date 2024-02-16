from pyosint.core.categories.company import Company
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://checko.ru"


class Checko(Company):
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
            temp_id = self.get_all_elements_from_parent(temp_dict['info'], 'a')[0].get('href')
            temp_dict['url'] = f"{URL}{temp_id}"
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
        return f"{URL}/search/quick_tips?query={input_data}"

    def get_brief_info(self, url):
        parsed = self.get_parsed_object(url)
        brief_info_dict = dict()
        brief_info_div = self.get_all_elements_from_parent(parsed, 'div',
                                                           attributes={'class': 'uk-width-1 uk-width-1-2@m'})[1]
        brief_info_subdivs = self.get_all_elements_from_parent(brief_info_div, 'div', recursive=False)[2:]
        temp_text_list = self.parse_strings_list(brief_info_subdivs)
        for temp_text_el in temp_text_list:
            temp_title = temp_text_el[0]
            temp_text = temp_text_el[1:]
            if len(temp_text) == 1:
                temp_text = temp_text[0]
            brief_info_dict[temp_title] = temp_text
        return self.flatten_card_data(brief_info_dict)

    def get_contact_info(self, url):
        parsed = self.get_parsed_object(url)
        parsed_text = self.parse_strings_list(
            self.get_all_elements_from_parent(parsed, 'section', {'class': "extra-section"}))
        return parsed_text[:-3]

    def get_ids_info(self, url):
        parsed = self.get_parsed_object(url)
        ids_data = self.get_all_elements_from_parent(parsed, 'tr')
        ids_info = []
        for tr in ids_data:
            ids_info.append(self.parse_strings_list(tr))
        return ids_info

    def get_company_sphere_info(self, url, key, page=None, headers=None, params=None, collection_type='dict'):
        info_dict = {key: {}}

        if page is None:
            page = key

        parsing_urls = [url + f"?extra={page}&type={param}" for param in params] if params else [url + f"?extra={page}"]
        params = params if params else [None] * len(parsing_urls)
        for parsing_url, param in zip(parsing_urls, params):
            parsed = self.get_parsed_object(parsing_url)
            tables = self.get_all_elements_from_parent(parsed, 'table')
            if key == 'finances':
                tables = tables[-5:]
            headers = headers if headers else [None] * len(tables)
            table = []

            if len(tables) != 0:
                for row_table in tables:
                    trs = self.get_all_elements_from_parent(row_table, 'tr')
                    table.append(self.parse_table(trs, collection_type=collection_type))

            table = self.flatten_card_data(table)
            if any(params):
                info_dict[key][param] = table
            else:
                info_dict[key] = table
        return self.flatten_card_data(info_dict)

    def get_company_info(self, url):
        info_dict = dict()
        info_dict["info"] = self.get_brief_info(url)
        info_dict["contact"] = self.get_contact_info(url + "?extra=contacts")

        info_dict.update({"ids": self.get_ids_info(url + "?extra=details")})
        info_dict.update(self.get_company_sphere_info(
            url, 'connections', params=["management", "founders", "managed", "founded", "predecessors", "successors"]))

        simple_tables = ["finances", "contracts",
                         "inspections", "legal-cases", "enforcements", "fedresurs", "licenses", "branches", "activity"]
        for simple_table in simple_tables:
            info_dict.update(self.get_company_sphere_info(url, simple_table))
        return self.flatten_card_data(info_dict)


def main():
    handle_cmd_args_module(Checko)


if __name__ == "__main__":
    main()
