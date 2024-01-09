from pyosint.core.templates.web import Web

URL = "https://columbus.elmasy.com"


class Elmasy(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/report/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        subdomains = list()
        h2 = self.get_all_elements_from_parent(parsed,
                                               'h2',
                                               {"class": "self-start max-lg:text-xl lg:text-2xl"})
        h2_text_list = [el.replace("\n", "").replace("-> ", "") for el in self.get_element_text(h2)]
        for h2_text in h2_text_list:
            temp_div = self.get_all_elements_from_parent(parsed, 'div', {"id": h2_text})[0]
            temp_table = self.get_all_elements_from_parent(temp_div, 'table')
            if len(temp_table) == 1:
                trs = self.get_all_elements_from_parent(temp_table[0], 'tr')
                ths = self.get_element_text(self.get_all_elements_from_parent(temp_table[0], 'th'))
                parsed_table = self.parse_table(trs, headers=ths, first_row_index=1)
                subdomains.append({h2_text: parsed_table})
            else:
                subdomains.append({h2_text: ''})
        return subdomains


def main():
    pass


if __name__ == "__main__":
    main()
