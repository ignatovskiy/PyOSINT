from pyosint.core.categories.person import Person
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.peekyou.com"


class PeekYou(Person):
    types = ["nickname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url) -> dict:
        return self.make_request('post', url, data_={"username": self.input_data}).json()

    def get_search_url(self, input_data):
        return f"{URL}/web_results/fetchaliasres.php"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        sites_list = parsed['response']
        complex_data = {}
        for site_id in sites_list.keys():
            site = sites_list[site_id]
            status = site['status']
            url = site['url']
            if status != 'Available':
                complex_data[site['site']] = url
        return complex_data


def main():
    handle_cmd_args_module(PeekYou)


if __name__ == "__main__":
    main()
