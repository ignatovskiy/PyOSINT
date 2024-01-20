from pyosint.core.categories.web import Web


URL = "https://analyzeid.com"


class AnalyzeID(Web):
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/id/{input_data}"

    def get_complex_data(self):
        url = self.get_search_url(self.input_data)
        parsed = self.get_parsed_object(url)
        table = self.get_all_elements_from_parent(parsed, 'table')
        if table:
            trs = self.get_all_elements_from_parent(table[0], 'tr')
            ths = self.parse_strings_list(self.get_all_elements_from_parent(trs[0], 'th'))
            site_info = self.parse_table(trs, do_list=True)
            if site_info:
                return dict(zip(ths, site_info[0]))
            else:
                return None
        else:
            return None


def main():
    pass  # U-NW


if __name__ == "__main__":
    main()
