from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://securityheaders.com"


class SecurityHeaders(Web):
    types = ["ip", "hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/?followRedirects=on&q={input_data}"

    def get_whois(self):
        url = self.get_search_url(input_data=self.input_data)
        parsed = self.get_parsed_object(url)
        tables = self.get_all_elements_from_parent(parsed, 'table')
        headers = self.parse_strings_list(self.get_all_elements_from_parent(parsed,
                                                                            'div',
                                                                            {"class": "reportTitle"}))

        try:
            headers.remove('Supported By')
        except ValueError:
            pass

        rows = []
        for i, table in enumerate(tables):
            tds = self.parse_strings_list(self.get_all_elements_from_parent(table, 'td'))
            if i == 0:
                tds = tds[:-2]
            ths = self.get_all_elements_from_parent(table, 'th')
            if not ths:
                continue
            parsed_rows = self.parse_table(tds, headers=ths, tds_ready=True, first_row_index=1)
            rows.append(parsed_rows)
        new_rows = [el for el in rows if el]
        return dict(zip(headers, new_rows))

    def get_complex_data(self):
        complex_data = self.get_whois()
        return complex_data


def main():
    handle_cmd_args_module(SecurityHeaders)


if __name__ == "__main__":
    main()
