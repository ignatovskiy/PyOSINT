import random

from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://typosquatting-finder.circl.lu"


class TypoSquattingFinder(Web):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        boundary = str(random.randint(100000, 999999))
        url_data = f"""\nContent-Disposition: form-data; name="url"\n\n"""
        submit_data = f"""\nContent-Disposition: form-data; name="runall"\n\n"""
        ns_data = f"""\nContent-Disposition: form-data; name="NS"\n\n"""
        mx_data = f"""\nContent-Disposition: form-data; name="MX"\n\n"""
        file_data = f"""\nContent-Disposition: form-data; name="file_1"\n\n"""
        bd = f"------{boundary}"
        runall_data = "runall"
        undefined_data = "undefined"

        first_text_part = f"""{bd}{url_data}{self.input_data}\n{bd}{submit_data}{runall_data}\n"""
        second_text_part = f"""{bd}{ns_data}\n{bd}{mx_data}\n{bd}{file_data}{undefined_data}\n{bd}--\n"""
        text_data = f"{first_text_part}{second_text_part}"
        headers = {
            'Content-Type': f'multipart/form-data; boundary=----{boundary}',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "522",
            "Host": "typosquatting-finder.circl.lu",
            "Origin": "https://typosquatting-finder.circl.lu",
            "Referer": "https://typosquatting-finder.circl.lu/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        return self.get_request_content(self.make_request('post',
                                                          url,
                                                          data_=text_data,
                                                          new_headers=headers), return_json=True)

    def get_search_url(self):
        return f"{URL}/typo"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url())
        print(parsed)
        parsed_uri = parsed['id']
        result_url = f"{URL}/domains/{parsed_uri}"
        headers = {"Accept": "*/*",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "en-US,en;q=0.9",
                   "Connection": "keep-alive",
                   "Host": "typosquatting-finder.circl.lu",
                   "Referer": "https://typosquatting-finder.circl.lu/"}
        result_url = f"{URL}/status/{parsed_uri}"
        complex_data = self.get_request_content(self.make_request('get',
                                                                  result_url,
                                                                  pre_sleep=5, new_headers=headers), return_json=True)
        complex_data = self.get_request_content(self.make_request('get',
                                                                  result_url,
                                                                  pre_sleep=5, new_headers=headers), return_json=True)
        complex_data = self.get_request_content(self.make_request('get',
                                                                  result_url,
                                                                  pre_sleep=5, new_headers=headers), return_json=True)
        complex_data = self.get_request_content(self.make_request('get',
                                                                  result_url,
                                                                  pre_sleep=5, new_headers=headers), return_json=True)
        complex_data = self.get_request_content(self.make_request('get',
                                                                  result_url,
                                                                  pre_sleep=5, new_headers=headers), return_json=True)
        result_url = f"{URL}/domains/{parsed_uri}"
        complex_data = self.get_request_content(self.make_request('get',
                                                                  result_url,
                                                                  pre_sleep=60, new_headers=headers), return_json=True)
        return complex_data


def main():
    handle_cmd_args_module(TypoSquattingFinder)


if __name__ == "__main__":
    main()
