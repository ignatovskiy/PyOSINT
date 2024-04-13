from concurrent.futures import ThreadPoolExecutor, as_completed

from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


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

    def process_list_element(self, h2_text, parsed_):
        temp_table = parsed_.find('div', {"id": h2_text}).find('table')
        if temp_table:
            trs = self.get_all_elements_from_parent(temp_table, 'tr')
            ths = self.get_all_elements_from_parent(temp_table, 'th')
            parsed_table = self.parse_table(trs, headers=ths, first_row_index=1)
            return {h2_text: parsed_table}
        else:
            return {h2_text: ''}

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        h2 = self.get_all_elements_from_parent(parsed,
                                               'h2',
                                               {"class": "self-start max-lg:text-xl lg:text-2xl"})
        h2_text_list = [el[1] for el in self.parse_strings_list(h2)]

        subdomains = []

        with ThreadPoolExecutor() as executor:
            futures = (executor.submit(self.process_list_element, h2_text, parsed) for h2_text in h2_text_list)

            for future in as_completed(futures):
                try:
                    subdomains.append(future.result())
                except Exception:
                    pass

        complex_data = {"Subdomains": h2_text_list, "Detailed": subdomains}
        return complex_data


def main():
    handle_cmd_args_module(Elmasy)


if __name__ == "__main__":
    main()
