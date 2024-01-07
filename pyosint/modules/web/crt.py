from pyosint.core.templates.web import Web

URL = "https://crt.sh"


class Crt(Web):
    types = ["ip", "hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get',
                                                                                 url,
                                                                                 use_default_headers=False)))

    def get_search_url(self, input_data):
        return f"{URL}/?q={input_data}"

    def get_complex_data(self):
        url = self.get_search_url(self.input_data)
        parsed = self.get_parsed_object(url)
        table = self.get_all_elements_from_parent(parsed, 'table')
        if table:
            table = table[-1]
            trs = self.get_all_elements_from_parent(table, 'tr')
            parsed_table = self.parse_table(trs)
            try:
                combined_dict = {}
                for dict_ in parsed_table:
                    combined_dict.update(dict_)
                return combined_dict
            except ValueError:
                return parsed_table
        else:
            return None


def main():
    pass


if __name__ == "__main__":
    main()
