from pyosint.core.categories.file import File
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://libgen.rs"


class Libgen(File):
    types = ['filename']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/search.php?req={input_data}&open=0&res=100&view=simple&phrase=1&column=def"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        table = self.get_all_elements_from_parent(parsed, 'table', {"rules": "rows"})[0]
        trs = self.get_all_elements_from_parent(table, 'tr')
        ths = self.parse_strings_list(trs[0])[:-2] + ['Mirror 1', 'Mirror 2', 'Edit']
        trs = trs[1:]
        complex_data = self.parse_table(trs, headers=ths, first_row_index=1)
        for index in range(len(complex_data)):
            links = [el.get('href') for el in self.get_all_elements_from_parent(trs[index], 'a')]
            link1, link2 = links[-3:-1]
            complex_data[index]["Mirror 1"] = link1
            complex_data[index]["Mirror 2"] = link2
            if complex_data[index].get('Edit'):
                del complex_data[index]["Edit"]
        return complex_data


def main():
    handle_cmd_args_module(Libgen)


if __name__ == "__main__":
    main()
