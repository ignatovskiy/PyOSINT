from pyosint.core.categories.file import File
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://yourbittorrent.com"


class YourBittorrent(File):
    types = ['filename']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/?v=&c=&q={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        table = self.get_all_elements_from_parent(parsed, 'table')[-1]
        links = [link.get('href') for link in self.get_all_elements_from_parent(table, 'a')]
        trs = self.get_all_elements_from_parent(table, 'tr')
        ths = self.get_all_elements_from_parent(table, 'th')
        complex_data = self.parse_table(trs, headers=ths, first_row_index=1)
        for table, link in zip(complex_data, links):
            table['Name'] = " ".join(table['Name'])
            table['Link'] = f"https://yt.0c.mom/down/{link.split('/')[2]}.torrent"
        return complex_data


def main():
    handle_cmd_args_module(YourBittorrent)


if __name__ == "__main__":
    main()
