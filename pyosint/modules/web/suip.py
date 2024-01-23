import random

from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://suip.biz"


class Suip(Web):
    types = ['hostname']

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url, headers, data):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('post',
                                                                                 url,
                                                                                 new_headers=headers,
                                                                                 data_=data)))

    def get_search_url(self):
        return f"{URL}/?act=subfinder"

    def get_complex_data(self):
        boundary = str(random.randint(1000, 9999))
        new_headers = {'Content-Type': f'multipart/form-data; boundary=--{boundary}'}
        url_data = f"""\nContent-Disposition: form-data; name="url"\n\n"""
        submit_data = f"""\nContent-Disposition: form-data; name="Submit1"\n\nSubmit"""
        text_data = f"""----{boundary}{url_data}{self.input_data}\n----{boundary}{submit_data}"""

        parsed = self.get_parsed_object(self.get_search_url(), new_headers, text_data)
        pre = self.get_all_elements_from_parent(parsed, 'pre')[0]
        complex_data = pre.get_text().split('\n')
        return complex_data[:-1]


def main():
    handle_cmd_args_module(Suip)


if __name__ == "__main__":
    main()
