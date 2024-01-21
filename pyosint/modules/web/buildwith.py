from pyosint.core.cmd import handle_cmd_args_module
from pyosint.core.categories.web import Web

URL = "https://builtwith.com"


class BuildWith(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/?q={input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        divs = self.get_all_elements_from_parent(parsed, 'div', {"class": "row mb-1 mt-1"})
        complex_data = []

        for div in divs:
            title = self.parse_strings_list(self.get_all_elements_from_parent(div, 'h2'))
            desc = self.parse_strings_list(self.get_all_elements_from_parent(div, 'p', {"class": "pb-0 mb-0 small"}))
            category = self.parse_strings_list(
                self.get_all_elements_from_parent(div, 'p', {"class": "small text-muted"}))

            temp_dict = {
                "Technology": title,
                "Description": desc,
            }
            if len(category) > 0 and category[0]:
                temp_dict.update({"Category": category})

            complex_data.append(temp_dict)
        return complex_data


def main():
    handle_cmd_args_module(BuildWith)


if __name__ == "__main__":
    main()
