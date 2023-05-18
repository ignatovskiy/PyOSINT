from pyosint.core.utils import *


URL = "https://securityheaders.com/?followRedirects=on&q="


class SecurityHeaders:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}{input_data}"

    def get_whois(self):
        url = self.get_search_url(input_data=self.input_data)
        parsed = self.get_parsed_object(url)
        tables = get_all_elements_from_parent(parsed, 'table')
        rows = list()
        headers = get_element_text(get_all_elements_from_parent(parsed, 'div', {"class": "reportTitle"}))
        headers.remove('Supported By')
        for table in tables:
            trs = get_all_elements_from_parent(table, 'tr')
            parsed_rows = parse_table(trs, parsed, th_key=True, first_row_index=1)
            rows.append(parsed_rows)
        rows = [el for el in rows if el]
        return dict(zip(headers, rows))

    def get_site_info(self):
        whois = self.get_whois()
        return whois


def main():
    pass


if __name__ == "__main__":
    main()
