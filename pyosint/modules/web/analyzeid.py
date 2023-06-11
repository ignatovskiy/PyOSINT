from pyosint.core.utils import *


URL = "https://analyzeid.com/id"


class TemplateWeb:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/{input_data}"

    def get_complex_data(self):
        url = self.get_search_url(self.input_data)
        parsed = self.get_parsed_object(url)
        table = get_all_elements_from_parent(parsed, 'table')
        if table:
            trs = get_all_elements_from_parent(table[0], 'tr')
            ths = get_element_text(get_all_elements_from_parent(trs[0], 'th'))
            site_info = parse_table(trs, parsed, do_list=True)
            if site_info:
                return dict(zip(ths, site_info[0]))
            else:
                return None
        else:
            return None


def main():
    pass


if __name__ == "__main__":
    main()
