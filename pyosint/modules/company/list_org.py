from pyosint.core.recognizer import Recognizer
from pyosint.core.utils import *


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
                lists_of_orgs.extend(get_all_elements_from_parent(self.get_parsed_object(url), 'p'))
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
        return get_soup_from_raw(get_request_content(make_request('get', url)))

    def get_company_info(self, url):
        info_dict = dict()

        parsed = self.get_parsed_object(url)

        brief_card = get_all_elements_from_parent(parsed, 'div', attributes={'class': 'card w-100 p-1 p-lg-3 mt-1'})
        if brief_card and len(brief_card) > 1:
            brief_ps = get_all_elements_from_parent(brief_card[1], 'tr')
            brief_dict = get_text_from_ps(brief_ps, clean_key=True)
            info_dict.update(brief_dict)

        cards = get_all_elements_from_parent(parsed, 'div', attributes={'class': 'card w-100 p-1 p-lg-3 mt-2'})

        for card in cards:
            h6_element = get_all_elements_from_parent(card, 'h6')
            if h6_element:
                h6 = get_element_text(h6_element[0])
            else:
                continue
            h6 = clean_attr(h6, attr_type='key')
            info_dict[h6] = list()
            if card.table:
                headers = []

                table = get_all_elements_from_parent(card, 'table')[0]
                trs = get_all_elements_from_parent(table, 'tr')

                first_row_index = 0

                for tr in trs:
                    first_row_index += 1
                    tth_elements = get_all_elements_from_parent(tr, 'td', attributes={"class": "tth"})
                    if tth_elements:
                        headers = get_element_text(tth_elements)
                        break

                if not headers:
                    first_row_index = 0

                rows_list = parse_table(trs[first_row_index:], parsed, collection_type='list',
                                        first_row_index=first_row_index, headers=headers)
                if rows_list:
                    info_dict[h6].append(rows_list)

            ps = get_all_elements_from_parent(card, 'p')
            ps_dict = get_text_from_ps(ps, clean_key=True, clean_value=True)
            if ps_dict:
                info_dict[h6].append(ps_dict)

            card_data = info_dict[h6]
            info_dict[h6] = flatten_card_data(card_data)
        return info_dict


def main():
    pass


if __name__ == "__main__":
    main()
