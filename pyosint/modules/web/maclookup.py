from pyosint.core.templates.web import Web

URL = "https://maclookup.app"


class MacLookup(Web):
    types = ["id"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/search/result?mac={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        div = self.get_all_elements_from_parent(parsed, 'div', {"class": "oui-group"})[0]
        ps = self.get_element_text(self.get_all_elements_from_parent(div, 'p'))
        return ps


def main():
    pass


if __name__ == "__main__":
    main()
