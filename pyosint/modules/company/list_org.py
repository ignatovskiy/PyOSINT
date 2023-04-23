from pyosint.core.parser import Parser
from pyosint.core.recognizer import Recognizer

URL = "https://www.list-org.com"

NAME = 'name'
INN = 'inn'
OGRN = 'ogrn'
OKPO = 'okpo'
ADDRESS = 'address'
HEAD = 'boss'
PHONE = 'phone'

DATA_TYPES = {
    'company': [NAME],
    'id': [INN, OGRN, OKPO],
    'address': [ADDRESS],
    'name': [HEAD],
    'phone': [PHONE]
}


class ListOrg:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type] if data_type else self.get_input_data_type()

    def get_input_data_type(self):
        return set(Recognizer(self.input_data).get_data_types_list()).intersection(DATA_TYPES.keys())

    def get_lists_of_orgs(self):
        lists_of_orgs = []
        for data_type in self.data_type:
            urls = self.get_search_urls(data_type, self.input_data)
            for url in urls:
                lists_of_orgs.extend(self.get_parsed_object(url).get_all_elements('p'))
        return set(lists_of_orgs)

    def get_search_results(self):
        results = []
        for org in self.get_lists_of_orgs():
            if org.span:
                span_data = org.span.text
                span_data = span_data.replace("инн/кпп: ", '|||').replace("юр.адрес: ", '|||')
                span_data_list = span_data.split("|||")

                if len(span_data_list) == 3:
                    link_data = org.label.a

                    company_name = link_data.text
                    company_link = link_data.get('href')

                    company_fullname, company_ids, company_address = span_data.split("|||")
                    company_inn, company_kpp = company_ids.split("/")

                    results.append({
                        "company": company_name,
                        "company_fullname": company_fullname,
                        "address": company_address,
                        "id_kpp": company_kpp,
                        "id_inn": company_inn,
                        "url": URL + company_link
                    })
        return results

    def get_complex_data(self):
        search_results = self.get_search_results()
        complex_data = []

        for result in search_results:
            complex_data.append(self.get_company_info(result['url']))

        return complex_data

    @staticmethod
    def get_search_url(data_type, input_data):
        return f"{URL}/search?type={data_type}&val={input_data}"

    def get_search_urls(self, data_type, input_data):
        urls_list = []
        for type_ in DATA_TYPES[data_type]:
            urls_list.append(self.get_search_url(type_, input_data))
        return urls_list

    @staticmethod
    def get_parsed_object(url):
        return Parser(url, 'get')

    @staticmethod
    def get_cells_data(first_row_index, headers, tds):
        if first_row_index >= 1:
            if len(headers) == len(tds):
                return dict(zip(headers, tds))
            else:
                return None
        elif first_row_index == 0:
            if len(tds) == 2:
                return {tds[0]: tds[1]}
            elif len(tds) > 2:
                return {tds[0]: tds[1:]}
            else:
                return tds[0]

    @staticmethod
    def flatten_card_data(card_data):
        if len(card_data) == 1:
            if isinstance(card_data[0], dict):
                return card_data[0]
            elif isinstance(card_data[0], list) and isinstance(card_data[0][0], dict):
                if len(card_data[0]) == 1:
                    return card_data[0][0]
                else:
                    return card_data[0]
        return card_data

    @staticmethod
    def get_text_from_ps(ps):
        ps_dict = dict()
        for p in ps:
            if p.i:
                data_key = p.i.text.strip()
                data_value = p.text.replace(p.i.text, '').strip()

                if data_value:
                    ps_dict[data_key] = data_value
        return ps_dict

    def get_company_info(self, url):
        info_dict = dict()

        parsed = self.get_parsed_object(url)

        cards = parsed.get_all_elements('div', {'class': 'card w-100 p-1 p-lg-3 mt-2'})
        for card in cards:
            h6 = parsed.get_element_text(parsed.get_all_elements('h6', parent_element=card)[0])
            info_dict[h6] = list()
            if card.table:
                rows_list = []
                headers = []

                table = parsed.get_all_elements('table', parent_element=card)[0]
                trs = parsed.get_all_elements('tr', parent_element=table)

                first_row_index = 0

                for tr in trs:
                    first_row_index += 1
                    tth_elements = parsed.get_all_elements("td", {"class": "tth"}, parent_element=tr)
                    if tth_elements:
                        headers = parsed.get_element_text(tth_elements)
                        break

                for tr in trs[first_row_index:]:
                    tds_list = parsed.get_all_elements('td', parent_element=tr)
                    tds_text_list = parsed.get_element_text(tds_list)
                    row_list_element = self.get_cells_data(first_row_index, headers, tds_text_list)
                    if row_list_element:
                        rows_list.append(row_list_element)
                if rows_list:
                    info_dict[h6].append(rows_list)

            ps = parsed.get_all_elements('p', parent_element=card)
            ps_dict = self.get_text_from_ps(ps)
            if ps_dict:
                info_dict[h6].append(ps_dict)

            card_data = info_dict[h6]
            info_dict[h6] = self.flatten_card_data(card_data)
        return info_dict


def main():
    a = ListOrg('yandex').get_company_info("https://www.list-org.com/company/5308358")
    print(a)


if __name__ == "__main__":
    main()
