from pyosint.core.recognizer import Recognizer
from pyosint.core.templates.company import Company

URL = "https://www.list-org.com"

NAME = 'name'
INN = 'inn'
OGRN = 'ogrn'
OKPO = 'okpo'
ADDRESS = 'address'
HEAD = 'boss'
PHONE = 'phone'

TYPES = {
    'company': [NAME],
    'id': [INN, OGRN, OKPO],
    'address': [ADDRESS],
    'name': [HEAD],
    'phone': [PHONE]
}


class ListOrg(Company):
    types = ["company", "id"]

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type] if data_type else self.get_input_data_type()

    def get_input_data_type(self):
        return set(Recognizer(self.input_data).get_data_types_list()).intersection(TYPES.keys())

    def get_lists_of_orgs(self):
        lists_of_orgs = []
        for data_type in self.data_type:
            urls = self.get_search_urls(data_type, self.input_data)
            for url in urls:
                lists_of_orgs.extend(self.get_all_elements_from_parent(self.get_parsed_object(url), 'p'))
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

    def get_search_url(self, *args):
        return f"{URL}/search?type={args[0]}&val={args[1]}"

    def get_search_urls(self, data_type, input_data):
        urls_list = []
        for type_ in TYPES[data_type]:
            urls_list.append(self.get_search_url(type_, input_data))
        return urls_list

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_company_info(self, url):
        info_dict = dict()

        parsed = self.get_parsed_object(url)

        brief_card = self.get_all_elements_from_parent(parsed, 'div',
                                                       attributes={'class': 'card w-100 p-1 p-lg-3 mt-1'})
        if brief_card and len(brief_card) > 1:
            brief_ps = self.get_all_elements_from_parent(brief_card[1], 'tr')
            brief_dict = self.get_text_from_ps(brief_ps, clean_key=True)
            info_dict.update(brief_dict)

        cards = self.get_all_elements_from_parent(parsed,
                                                  'div',
                                                  attributes={'class': 'card w-100 p-1 p-lg-3 mt-2'})

        for card in cards:
            h6_element = self.get_all_elements_from_parent(card, 'h6')
            if h6_element:
                h6 = self.get_element_text(h6_element[0])
            else:
                continue
            h6 = self.clean_attr(h6, attr_type='key')
            info_dict[h6] = list()
            if card.table:
                headers = []

                table = self.get_all_elements_from_parent(card, 'table')[0]
                trs = self.get_all_elements_from_parent(table, 'tr')

                first_row_index = 0

                for tr in trs:
                    first_row_index += 1
                    tth_elements = self.get_all_elements_from_parent(tr, 'td', attributes={"class": "tth"})
                    if tth_elements:
                        headers = self.get_element_text(tth_elements)
                        break

                if not headers:
                    first_row_index = 0

                rows_list = self.parse_table(trs[first_row_index:], collection_type='list',
                                             first_row_index=first_row_index, headers=headers)
                if rows_list:
                    info_dict[h6].append(rows_list)

            ps = self.get_all_elements_from_parent(card, 'p')
            ps_dict = self.get_text_from_ps(ps, clean_key=True, clean_value=True)
            if ps_dict:
                info_dict[h6].append(ps_dict)

            card_data = info_dict[h6]
            info_dict[h6] = self.flatten_card_data(card_data)
        return info_dict


def main():
    pass


if __name__ == "__main__":
    main()
