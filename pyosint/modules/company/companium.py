from pyosint.core.categories.company import Company

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
            temp_dict['info'] = self.get_element_text(temp_dict['info'])
            results.append(temp_dict)
        return results

    def get_complex_data(self):
        search_results = self.get_search_results()
        complex_data = []

        for result in search_results:
            complex_data.append(self.get_company_info(result['url']))

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
        for brief_info_subdiv in brief_info_subdivs:
            temp_text_list = [el for el in self.get_element_text(brief_info_subdiv).split('\n') if el]
            temp_title = temp_text_list[0]
            temp_text = temp_text_list[1:]
            if len(temp_text) == 1:
                temp_text = temp_text[0]
            brief_info_dict[temp_title] = temp_text
        return brief_info_dict

    def get_contact_info(self, url):
        parsed = self.get_parsed_object(url)
        contact_info_dict = dict()
        contact_info_divs = self.get_all_elements_from_parent(parsed, 'div', attributes={'class': 'col-12 col-lg-4'})
        contact_info_divs.extend(self.get_all_elements_from_parent(parsed, 'div',
                                                                   attributes={
                                                                       'class': 'col-12 col-lg-4 border-lg-start'}))
        for contact_info_div in contact_info_divs:
            contact_info_header = self.get_element_text(
                self.get_all_elements_from_parent(contact_info_div, 'strong'))
            if not contact_info_header:
                contact_info_header = self.get_element_text(
                    self.get_all_elements_from_parent(contact_info_div, 'div', attributes={'class': 'fw-bold mb-1'}))
            contact_info_list = self.get_element_text(
                self.get_all_elements_from_parent(contact_info_div, 'a'))
            if contact_info_header[0] == 'Электронная почта':
                website_link = contact_info_list[-1]
                contact_info_dict['Веб-сайт'] = website_link
                contact_info_list = contact_info_list[:-1]
            contact_info_dict[contact_info_header[0]] = contact_info_list
        return contact_info_dict

    def get_company_sphere_info(self, url, key, page=None, headers=None, params=None):
        info_dict = {key: dict()}
        if page is None:
            page = key
        if params:
            for param in params:
                parsed = self.get_parsed_object(url + f"/{page}?type={param}")
                info_dict[key][param] = self.get_table_dict(parsed, headers)
        else:
            parsed = self.get_parsed_object(url + f"/{page}")
            info_dict[key] = self.get_table_dict(parsed, headers)
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
    pass


if __name__ == "__main__":
    main()
