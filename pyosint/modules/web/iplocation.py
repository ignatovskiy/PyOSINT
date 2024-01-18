from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.iplocation.net"

DATA_SOURCES = ["ipbase", "criminalip", "ipapico", "ipgeolocation", "ipregistry", "dbip", "ipinfo", "ip2location"]


class IpLocation(Web):
    types = ["ip"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url, source):
        data_dict = {
            "MIME Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "ip": self.input_data,
            "source": source,
            "ipv": "4"
        }

        try:
            raw_json_dict = self.make_request('post', url, data_=data_dict).json()
            json_dict = raw_json_dict['res']
            if json_dict.get('data'):
                json_dict = json_dict['data']
        except AttributeError:
            return dict()
        return json_dict

    def get_search_url(self, input_data):
        return f"{URL}/get-ipdata"

    def get_complex_data(self):
        data_sources = ["ipbase", "criminalip", "ipapico", "ipgeolocation", "ipregistry", "dbip", "ipinfo",
                        "ip2location"]
        complex_data = {}
        exclusions = [None, "", "This parameter is unavailable in selected .BIN data file. Please upgrade."]

        def process_category(data_source):
            parsed_dict = self.get_parsed_object(self.get_search_url(self.input_data), data_source)
            complex_data[data_source] = {key: value for key, value in parsed_dict.items() if value not in exclusions}

        self.process_requests_concurrently(process_category, reqs=data_sources)
        return complex_data


def main():
    handle_cmd_args_module(IpLocation)


if __name__ == "__main__":
    main()
