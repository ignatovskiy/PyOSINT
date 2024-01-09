import concurrent.futures

from pyosint.core.templates.web import Web

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
        data_dict = dict()

        def process_category(category):
            parsed = self.get_parsed_object(self.get_search_url(self.input_data, category))
            if categories[category]:
                facts = parsed[categories[category]]
                if category == "analysis":
                    facts_data = {key: value for key, value in facts.items() if value}
                    analysis_data = self.flatten_card_data(facts_data)
                    data_dict.update({"analysis": analysis_data})
                else:
                    facts_list = list()
                    facts_keys = ["address", "first", "last", "hostname", "record_type", "flag_title", "asn"]
                    for fact in facts:
                        facts_list.append({el: fact[el] for el in fact if el in facts_keys})
                    data_dict.update({"passive_dns": facts_list})
            else:
                data_dict.update({"geo": parsed})

        def process_categories_concurrently():
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(process_category, category): category for category in categories}

                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except TypeError:
                        pass
        process_categories_concurrently()
        return data_dict


def main():
    pass


if __name__ == "__main__":
    main()
