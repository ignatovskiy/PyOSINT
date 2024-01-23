from pyosint.core.categories.person import Person
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.steamidfinder.com"


class SteamIdFinder(Person):
    types = ["nickname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('post',
                                                                                 url,
                                                                                 data_={'steamid': self.input_data})))

    def get_search_url(self, input_data):
        return f"{URL}/lookup/"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        try:
            table = self.get_all_elements_from_parent(parsed, 'table', {'id': 'profile-info'})[0]
            trs = self.get_all_elements_from_parent(table, 'tr')
            ths = self.get_all_elements_from_parent(table, 'th')
            complex_data = self.parse_table(trs, headers=ths)
        except IndexError:
            return {}
        return complex_data


def main():
    handle_cmd_args_module(SteamIdFinder)


if __name__ == "__main__":
    main()
