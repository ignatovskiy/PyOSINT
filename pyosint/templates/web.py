from pyosint.core.utils import *


URL = ""


class TemplateWeb:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/{input_data}"

    def get_site_info(self):
        url = self.get_search_url(self.input_data)
        return url


def main():
    print(TemplateWeb("example.site").get_site_info())


if __name__ == "__main__":
    main()
