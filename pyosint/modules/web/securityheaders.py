from pyosint.core.templates.web import Web

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
        rows = list()
        headers = self.get_element_text(self.get_all_elements_from_parent(parsed, 'div', {"class": "reportTitle"}))
        try:
            headers.remove('Supported By')
        except ValueError:
            pass
        for table in tables:
            trs = self.get_all_elements_from_parent(table, 'tr')
            parsed_rows = self.parse_table(trs, th_key=True, first_row_index=1)
            rows.append(parsed_rows)
        rows = [el for el in rows if el]
        new_rows = list()
        for row in rows:
            combined_dict = {}
            for dict_ in row:
                combined_dict.update(dict_)
            new_rows.append(combined_dict)
        return dict(zip(headers, new_rows))

    def get_complex_data(self):
        whois = self.get_whois()
        return whois


def main():
    pass


if __name__ == "__main__":
    main()
