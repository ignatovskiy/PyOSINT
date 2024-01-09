import concurrent.futures

from pyosint.core.templates.web import Web

URL = "https://well-known.dev"


class WellKnown(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data, page):
        return f"{URL}/?q={input_data}&page={page}"

    def get_complex_data(self):
        data_list = list()

        def process_iteration(index):
            parsed = self.get_parsed_object(self.get_search_url(self.input_data, index))
            table = self.get_all_elements_from_parent(parsed, 'table', {"class": "responsive grid"})[0]
            trs = self.get_all_elements_from_parent(table, 'tr')
            ths = self.get_element_text(self.get_all_elements_from_parent(table, 'th'))
            table_data = self.flatten_card_data(self.parse_table(trs, headers=ths, first_row_index=1))
            data_list.append(table_data)
            disabled_next_page = self.get_all_elements_from_parent(parsed, "a", {"class": "disabled"})
            if disabled_next_page and "Next" in self.get_element_text(disabled_next_page):
                return True

        def process_while_loop_concurrently():
            index = 0
            with concurrent.futures.ThreadPoolExecutor() as executor:
                while True:
                    futures = [executor.submit(process_iteration, index)]

                    for future in concurrent.futures.as_completed(futures):
                        should_break = future.result()

                    if should_break:
                        break
                    else:
                        index += 1
        process_while_loop_concurrently()
        return data_list


def main():
    pass


if __name__ == "__main__":
    main()
