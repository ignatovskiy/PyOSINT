from pyosint.core.utils import *


URL = "https://osint.sh"


class OsintSH:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    @staticmethod
    def get_parsed_object(url):
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    @staticmethod
    def get_search_url(input_data):
        return f"{URL}/{input_data}"

    def get_certs_info(self):
        url = f"{URL}/crt/"
        request = make_request('post', url, data_={'domain': self.input_data})
        parsed = get_soup_from_raw(get_request_content(request))
        table = get_all_elements_from_parent(parsed, 'table')
        if table:
            table = table[0]
            trs = get_all_elements_from_parent(table, 'tr')
            parsed_table = parse_table(trs, parsed)
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
