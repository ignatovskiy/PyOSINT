from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = "https://host.io"


class HostIo(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data, category):
        return f"{URL}/{category}/{input_data}"

    def get_complex_data(self):
        categories = {"backlinks": "Backlinks sites", "redirects": "Redirects to sites",
                      "ip": "Sites on same IP", "asn": "Sites on same ASN"}
        span_class = "bg-gray-200 hover:bg-gray-300 text-gray-700 p-1 rounded-lg tracking-normal font-mono text-sm"
        complex_data = {}

        def process_category(category):
            temp_input_data = self.input_data
            if category in ["ip", "asn"]:
                parsed = self.get_parsed_object(self.get_search_url(self.input_data, ''))
                spans = self.get_all_elements_from_parent(parsed, 'span', {"class": span_class})
                input_data_list = [span.a.get('href') for span in spans]
                for input_data_el in input_data_list:
                    if category in input_data_el:
                        temp_input_data = input_data_el.replace(f"/{category}/", '')
                        break

            parsed = self.get_parsed_object(self.get_search_url(temp_input_data, category))
            lis = self.get_all_elements_from_parent(parsed,
                                                    'li',
                                                    {"class": "sm:w-1/3 w-1/2 border-b border-r px-6 py-4"})
            lis_text = self.parse_strings_list(lis)
            complex_data.update({categories[category]: lis_text})

        self.process_requests_concurrently(process_category, reqs=categories)
        return complex_data


def main():
    handle_cmd_args_module(HostIo)


if __name__ == "__main__":
    main()
