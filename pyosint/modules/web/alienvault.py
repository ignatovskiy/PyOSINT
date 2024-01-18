from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module

URL = "https://otx.alienvault.com"


class AlienVault(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.make_request('get', url).json()

    def get_search_url(self, input_data, category):
        return f"{URL}/otxapi/indicators/domain/{category}/{input_data}"

    def get_complex_data(self):
        categories = {"analysis": "facts", "passive_dns": "passive_dns", "geo": None}
        data_dict = {}

        def process_category(category):
            parsed = self.get_parsed_object(self.get_search_url(self.input_data, category))

            if category == "analysis":
                facts_data = {key: value for key, value in parsed.get(categories[category], {}).items() if value}
                analysis_data = self.flatten_card_data(facts_data)
                if analysis_data:
                    data_dict["analysis"] = analysis_data
            elif category == "passive_dns":
                facts_list = [
                    {el: fact[el] for el in fact if
                     el in ["address", "first", "last", "hostname", "record_type", "flag_title", "asn"]}
                    for fact in parsed.get(categories[category], [])
                ]
                if facts_list:
                    data_dict["passive_dns"] = facts_list
            else:
                geo_data = {key: value for key, value in parsed.items() if value}
                if geo_data:
                    data_dict["geo"] = geo_data

        self.process_requests_concurrently(process_category, reqs=categories)
        return data_dict


def main():
    handle_cmd_args_module(AlienVault)


if __name__ == "__main__":
    main()
