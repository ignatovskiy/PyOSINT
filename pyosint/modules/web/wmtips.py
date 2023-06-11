from pyosint.core.utils import *


URL = "https://www.wmtips.com/tools/info"


class WmTips:
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
        tables = get_all_elements_from_parent(parsed, 'table')
        rows = dict()
        section = 0
        for table in tables:
            trs = get_all_elements_from_parent(table, 'tr')
            temp_table = parse_table(trs, parsed, th_key=True)
            ths = get_element_text(get_all_elements_from_parent(table, 'th'))
            table_dict = dict(zip(ths, temp_table))
            if table_dict:
                rows[f"Section {section}"] = table_dict
            section += 1
        return rows


def main():
    pass


if __name__ == "__main__":
    main()
