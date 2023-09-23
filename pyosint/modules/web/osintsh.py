from pyosint.core.templates.web import Web

# cloudflare


URL = "https://osint.sh"


class OsintSH(Web):
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/{input_data}"

    def get_certs_info(self):
        url = f"{URL}/crt/"
        request = self.make_request('post', url, data_={'domain': self.input_data})
        parsed = self.get_soup_from_raw(self.get_request_content(request))
        table = self.get_all_elements_from_parent(parsed, 'table')
        if table:
            table = table[0]
            trs = self.get_all_elements_from_parent(table, 'tr')
            parsed_table = self.parse_table(trs, parsed)
            parsed_table = [el[''] for el in parsed_table]

            result_dict = dict()
            for list_ in parsed_table:
                result_dict[list_[0]] = list_[1:]
            return result_dict
        else:
            return None

    def get_complex_data(self):
        certs = self.get_certs_info()
        return certs


def main():
    pass


if __name__ == "__main__":
    main()
