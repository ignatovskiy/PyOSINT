from pyosint.core.templates.web import Web

URL = "https://www.mmnt.ru"


class MMNT(Web):
    types = ["filename"]  # TODO add filename to types

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/int/get?st={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        a_links = self.get_all_elements_from_parent(parsed, 'a', {"target": "_blank"})
        links = [a_link.get('href') for a_link in a_links]
        return links


def main():
    pass


if __name__ == "__main__":
    main()
