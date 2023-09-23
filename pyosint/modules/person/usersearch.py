from pyosint.core.templates.person import Person


URL = "https://usersearch.org/results_advanced.php"
PRE_URL = "https://usersearch.org/results_advanced"


class UserSearch(Person):
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}?URL_username={input_data}"

    def get_complex_data(self):
        ps = list()

        for i in range(0, 6):
            if i == 0:
                url = self.get_search_url(self.input_data)
            else:
                url = f"{PRE_URL}{str(i)}.php?URL_username={self.input_data}"
            parsed = self.get_parsed_object(url)
            divs_list = self.get_all_elements_from_parent(parsed, 'div', {"class": "results-item-content"})
            ps += [self.get_all_elements_from_parent(el, 'a')[0].get('href') for el in divs_list
                   if len(self.get_all_elements_from_parent(el, 'a')) > 0]
        return {"Found": ps}


def main():
    pass


if __name__ == "__main__":
    main()
