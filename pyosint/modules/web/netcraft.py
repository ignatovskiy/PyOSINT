from pyosint.core.templates.web import Web

URL = "https://sitereport.netcraft.com"


class NetCraft(Web):
    types = ["hostname"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        raw_page_content = self.get_request_content(self.make_request('get', url))
        page_content = raw_page_content.decode().replace('{"dmarc_table":"', "")[:-2]
        return self.get_soup_from_raw(page_content)

    def get_search_url(self, input_data):
        return f"{URL}/?url=https://{input_data}&ajax=dcg"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        data_list = list()
        tables = self.get_all_elements_from_parent(parsed, 'table')
        for table in tables:
            trs = self.get_all_elements_from_parent(table, 'tr')
            ths = self.get_element_text(self.get_all_elements_from_parent(table, 'th'))
            table_data = self.flatten_card_data(self.parse_table(trs, headers=ths, first_row_index=1))
            temp_table_data = list()
            if table_data:
                for table_el in table_data:
                    if isinstance(table_el, dict):
                        if table_el.get("Popular sites using this technology"):
                            del table_el["Popular sites using this technology"]
                        temp_table_data.append(table_el)
            if temp_table_data not in data_list:
                data_list.extend(temp_table_data)
        return data_list


def main():
    pass


if __name__ == "__main__":
    main()
