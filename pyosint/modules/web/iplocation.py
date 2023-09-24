from pyosint.core.templates.web import Web
import pyosint.core.reporter as Reporter

URL = "https://www.iplocation.net/get-ipdata"

DATA_SOURCES = ["ipbase", "criminalip", "ipapico", "ipgeolocation", "ipregistry", "dbip", "ipinfo", "ip2location"]


class IpLocation(Web):
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

        raw_json_dict = self.make_request('post', url, data_=data_dict).json()
        json_dict = raw_json_dict['res']
        if json_dict.get('data'):
            json_dict = json_dict['data']
        return json_dict

    def get_search_url(self, input_data):
        return URL

    def get_complex_data(self):
        complex_data = dict()
        for data_source in DATA_SOURCES:
            complex_data[data_source] = self.get_parsed_object(self.get_search_url(self.input_data), data_source)
        return complex_data


def main():
    a = IpLocation('7.7.7.7').get_complex_data()
    Reporter.generate_pdf_report(a, 'iplocation.pdf')


if __name__ == "__main__":
    main()
