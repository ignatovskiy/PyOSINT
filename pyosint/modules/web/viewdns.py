from pyosint.core.templates.web import Web

URL = "https://viewdns.info"


class ViewDns(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, section, input_data):
        return f"{URL}/{section}={input_data}"

    def get_complex_data(self):
        section = "dnsreport/?domain"
        parsed = self.get_parsed_object(self.get_search_url(section, self.input_data))
        try:
            table = self.get_all_elements_from_parent(parsed, 'table', {"border": "1"})[0]
            headers_tr = self.get_all_elements_from_parent(table, 'tr')[0]
            headers = self.get_element_text(self.get_all_elements_from_parent(headers_tr, 'td'))
            trs = self.get_all_elements_from_parent(table, 'tr')[1:]
            parsed_rows = self.parse_table(trs, headers=headers, first_row_index=1)
        except IndexError:
            return dict()
        return parsed_rows


def main():
    pass


if __name__ == "__main__":
    main()
