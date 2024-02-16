from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://www.tiny-scan.com"


class TinyScan(Web):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        data_dict = {
            "customHeaders": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            },
            "screenshotsResolutions": [
                "mobile",
                "desktop"
            ],
            "url": self.input_data,
            "visibility": "Public"
        }
        return self.get_request_content(self.make_request('post', url, json_=data_dict), return_json=True)

    def get_search_url(self, input_data):
        return f"{URL}/api/createScan"

    def get_complex_data(self):
        parsed: dict = self.get_parsed_object(self.get_search_url(self.input_data))
        uuid = parsed['data']['result']

        if uuid.get('uuid'):
            uuid = uuid['uuid']
        else:
            uuid = uuid['tasks'][0]['uuid']

        finish_url = f"{URL}/api/getScan"
        final_dict = {
            "uuid": uuid
        }
        complex_data = self.get_request_content(self.make_request('post',
                                                                  finish_url,
                                                                  json_=final_dict,
                                                                  pre_sleep=20),
                                                return_json=True)['data']['result']
        return complex_data


def main():
    handle_cmd_args_module(TinyScan)


if __name__ == "__main__":
    main()
