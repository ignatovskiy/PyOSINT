from pyosint.core.categories.file import File
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://bitsearch.to"


class BitSearch(File):
    types = ['filename']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/search?q={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        lis = self.get_all_elements_from_parent(parsed, 'li', {"class": "card search-result my-2"})
        complex_data = []

        for li in lis:
            temp_stats = self.parse_strings_list(
                             self.get_all_elements_from_parent(li,
                                                               'div',
                                                               {"class": "stats"})[0])

            temp_data = {"Title": self.parse_strings_list(self.get_all_elements_from_parent(li, 'h5')[0]),
                         "Downloads": temp_stats[0],
                         "Size": temp_stats[1],
                         "Seeders": temp_stats[2],
                         "Leechers": temp_stats[3],
                         "Date": temp_stats[4],
                         "Link": self.get_all_elements_from_parent(li,
                                                                   'a',
                                                                   {"class": "dl-torrent"})[0].get('href')}
            complex_data.append(self.flatten_card_data(temp_data))
        return complex_data


def main():
    handle_cmd_args_module(BitSearch)


if __name__ == "__main__":
    main()
