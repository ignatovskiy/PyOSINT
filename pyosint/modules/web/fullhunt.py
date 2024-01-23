from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://fullhunt.io"


class FullHunt(Web):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/search?query={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        divs = self.get_all_elements_from_parent(parsed, 'div', {"class": "card bg-gray mb-3"})
        complex_data = []
        for div in divs:
            temp_dict = dict()
            temp_dict["techs"] = self.parse_strings_list(
                self.get_all_elements_from_parent(div,
                                                  'div',
                                                  {"class": "col-md-12 mb-2"}))[:-1]
            temp_dict["provider"] = self.parse_strings_list(
                self.get_all_elements_from_parent(div,
                                                  'div',
                                                  {"class": "px-md-3 px-2 text-white-50"}))
            temp_dict["host"] = self.parse_strings_list(
                self.get_all_elements_from_parent(div,
                                                  'div',
                                                  {"class": "px-md-3 px-2 mb-2 text-gray"}))
            temp_dict["ports"] = self.parse_strings_list(
                self.get_all_elements_from_parent(div,
                                                  'div',
                                                  {"class": "ports"}))[1:]
            temp_dict["site"] = self.parse_strings_list(
                self.get_all_elements_from_parent(div,
                                                  'div',
                                                  {"class": "font-weight-bold d-inline-block pt-1 mb-2"}))
            complex_data.append(temp_dict)
        return complex_data


def main():
    handle_cmd_args_module(FullHunt)


if __name__ == "__main__":
    main()
