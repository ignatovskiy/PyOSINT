from pyosint.core.utils import *


URL = "https://www.peekyou.com/web_results/fetchaliasres.php"


class PeekYou:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return make_request('post', url, data_={"username": self.input_data}).json()

    @staticmethod
    def get_search_url(input_data):
        return URL

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        sites_list = parsed['response']
        sites_dict = dict()
        for site in sites_list:
            sites_dict[site['site']] = site['status']
        return sites_dict


def main():
    pass


if __name__ == "__main__":
    main()
