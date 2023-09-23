from pyosint.core.templates.web import Web

URL = "https://dnsdumpster.com/"


class DNSDumpster(Web):
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/?url={input_data}"

    def get_complex_data(self):
        parsed = self.get_csrf_site_content(URL, {'targetip': self.input_data, 'user': 'free'})
        tables = self.get_all_elements_from_parent(parsed, 'table')
        based_data = dict()
        headers = self.get_element_text(self.get_all_elements_from_parent(parsed, 'p',
                                                                {'style': "color: #ddd; font-family: 'Courier New', Courier, monospace; text-align: left;"}))
        for header, table in zip(headers, tables):
            trs = self.get_all_elements_from_parent(table, 'tr')
            parsed_table = self.parse_table(trs, parsed, do_list=True)
            header = header.split(" **")[0]
            based_data.update({header: parsed_table})
        return based_data


def main():
    pass


if __name__ == "__main__":
    main()
