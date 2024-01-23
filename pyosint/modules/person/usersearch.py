import time

from pyosint.core.categories.person import Person
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://usersearch.org"


class UserSearch(Person):
    types = ["nickname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/results_advanced.php?URL_username={input_data}"

    def get_complex_data(self):
        ps = set()

        def get_urls_list():
            urls_list = []
            bad_indexes = [3, 5, 6, 7]
            for i in range(0, 11):
                if i not in bad_indexes:
                    if i == 0:
                        url = self.get_search_url(self.input_data)
                    else:
                        url = f"{URL}/results_advanced{str(i)}.php?URL_username={self.input_data}"
                    urls_list.append(url)
            return urls_list

        def process_iteration(url):
            parsed = self.get_parsed_object(url)
            divs_list = self.get_all_elements_from_parent(parsed, 'div', {"class": "results-item-content"})
            [ps.add(self.get_all_elements_from_parent(el, 'a')[0].get('href')) for el in divs_list
             if len(self.get_all_elements_from_parent(el, 'a')) > 0]

        urls = get_urls_list()
        self.process_requests_concurrently(process_iteration, urls)
        complex_data = {"Found": list(ps)}
        return complex_data


def main():
    handle_cmd_args_module(UserSearch)


if __name__ == "__main__":
    main()
