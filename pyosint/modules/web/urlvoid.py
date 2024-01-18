from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.urlvoid.com"


class UrlVoid(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url, method='get', data=None):
        return self.get_soup_from_raw(self.get_request_content(self.make_request(method, url, data_=data)))

    def get_search_url(self, mode, input_data):
        return f"{URL}/{mode}/{input_data}"

    def get_complex_data(self):
        def clean_table(raw_table):
            useless_keys = ["Domain Information", "Reverse DNS"]
            for key in useless_keys:
                raw_table.pop(key)
            raw_table["Last Analysis"] = raw_table["Last Analysis"][0][:-2]
            raw_table["IP Address"] = raw_table["IP Address"][0]
            raw_table["Latitude / Longitude"] = raw_table["Latitude\\Longitude"][0]
            raw_table.pop("Latitude\\Longitude")
            return raw_table

        self.get_parsed_object(self.get_search_url('update', self.input_data),
                               method='post',
                               data={"update": True})
        parsed = self.get_parsed_object(self.get_search_url('scan', self.input_data))
        table = self.get_all_elements_from_parent(parsed,'table')[0]
        trs = self.get_all_elements_from_parent(table, 'tr')
        parsed_table = self.parse_table(trs)

        return clean_table(parsed_table)


def main():
    handle_cmd_args_module(UrlVoid)


if __name__ == "__main__":
    main()
