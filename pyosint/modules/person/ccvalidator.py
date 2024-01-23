from pyosint.core.categories.person import Person
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.ccvalidator.org"


class CcValidator(Person):
    types = ['id']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        data = {'bin': self.input_data}
        return self.get_csrf_site_content(URL, f'{URL}/bin-checker-result/', data)

    def get_search_url(self, input_data):
        return f"{URL}/bin-checker/"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        div = self.get_all_elements_from_parent(parsed,
                                                'div',
                                                {"class": "container w-50 glass-div p-3 my-5 text-light"})[0]
        ps = self.get_all_elements_from_parent(div, 'p')
        complex_data = []
        for p in ps:
            temp_text = self.parse_strings_list(p)
            complex_data.append(temp_text)
        complex_data = dict(zip(complex_data[0:4] + complex_data[8:12], complex_data[4:8] + complex_data[12:]))
        return complex_data


def main():
    handle_cmd_args_module(CcValidator)


if __name__ == "__main__":
    main()
