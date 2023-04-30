from pyosint.core.parser import Parser
from pyosint.core.utils import *

URL = "https://excheck.pro/company/"
COMPANY_URL = "https://excheck.pro/search/tips?query="


class Excheck:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_lists_of_orgs(self):
        url = self.get_search_url(self.input_data)
        orgs_dict = self.get_parsed_object(url).get_request().json()
        return orgs_dict

    def get_search_results(self):
        results = []
        for org in self.get_lists_of_orgs():
            temp_dict = org
            temp_dict['info'] = get_soup_from_raw(temp_dict['content'])
            temp_dict.pop('content')
            temp_dict['url'] = f"{URL}/{get_all_elements_from_parent(temp_dict['info'], 'a')[0].get('href')[9:]}"
            temp_dict['info'] = get_element_text(temp_dict['info'], sep_text=True)
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
        return Parser(url, 'get')

    @staticmethod
    def get_search_url(input_data):
        return f"{COMPANY_URL}{input_data}"

    def get_brief_info(self, url):
        parsed = self.get_parsed_object(url)
        brief_info_dict = dict()
        brief_info_div = parsed.get_all_elements('section', {'class': 'info-columns'})[0]
        brief_info_subdivs = parsed.get_all_elements('div', parent_element=brief_info_div, recursive=False)
        for brief_info_subdiv in brief_info_subdivs:
            temp_text_list = [el for el in get_element_text(brief_info_subdiv).split('\n') if el]
            temp_title = temp_text_list[0]
            temp_text = temp_text_list[1:]
            if len(temp_text) == 1:
                temp_text = temp_text[0]
            brief_info_dict[temp_title] = temp_text
        return brief_info_dict

    def get_company_sphere_info(self, url, key, page=None, headers=None, params=None):
        info_dict = {key: dict()}
        if page is None:
            page = key
        if params:
            for param in params:
                parsed = self.get_parsed_object(url + f"/{page}?type={param}")
                info_dict[key][param] = get_table_dict(parsed, headers)
        else:
            parsed = self.get_parsed_object(url + f"/{page}")
            info_dict[key] = get_table_dict(parsed, headers)
        return info_dict

    def get_company_info(self, url):
        info_dict = dict()
        info_dict["info"] = self.get_brief_info(url)
        info_dict.update(self.get_company_sphere_info(url, 'ids', page='details', headers='h1'))
        info_dict.update(self.get_company_sphere_info(
            url, 'connections', params=["management", "founders", "managed", "founded", "predecessors", "successors"]))

        simple_tables = ["licenses", "trademarks", "fedresurs", "contracts", "inspections", "legal-cases",
                         "activity", "enforcements", "finances", "branches"]
        for simple_table in simple_tables:
            info_dict.update(self.get_company_sphere_info(url, simple_table))
        return info_dict


def main():
    a = Excheck('5177746277385').get_company_info("https://excheck.pro/company/7736207543")
    print(a)


if __name__ == "__main__":
    main()
