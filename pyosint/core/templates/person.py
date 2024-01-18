from pyosint.core.categories.person import Person
from pyosint.core.cmd import handle_cmd_args_module


URL = ""


class PersonModule(Person):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        return parsed


def main():
    handle_cmd_args_module(PersonModule)


if __name__ == "__main__":
    main()
