from pyosint.core.categories.file import File
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.searchtor.to"


class SearchTor(File):
    types = ['filename']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/r/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        table = self.get_all_elements_from_parent(parsed, 'table', {"class": "pline"})[0]
        ths = self.get_all_elements_from_parent(table, 'th')
        trs = self.get_all_elements_from_parent(table, 'tr')
        complex_data = self.parse_table(trs, headers=ths, first_row_index=1)
        for index in range(len(complex_data)):
            temp_links = self.get_all_elements_from_parent(trs[index + 1], 'a')
            uri = temp_links[-1].get('href')
            theme = f"https:{temp_links[-3].get('href')}"
            temp_url = f"{URL}{uri}"
            complex_data[index]['Ссылка'] = temp_url
            complex_data[index]['Тема'] = theme
        return complex_data


def main():
    handle_cmd_args_module(SearchTor)


if __name__ == "__main__":
    main()
