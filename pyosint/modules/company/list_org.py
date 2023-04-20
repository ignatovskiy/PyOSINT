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


def get_search_url(data_type, input_data):
    return f"{URL}/search?type={data_type}&val={input_data}"


def get_search_urls(data_type, input_data):
    urls_list = []
    for type_ in DATA_TYPES[data_type]:
        urls_list.append(get_search_url(type_, input_data))
    return urls_list


def get_paragraphs(url):
    return Parser(url, 'get').get_all_elements('p')


def get_card(url):
    return Parser(url, 'get').get_all_elements('div', {'class': 'card w-100 p-1 p-lg-3 mt-2'})


def get_company_info(url):
    info_dict = dict()
    cards = get_card(url)
    for card in cards:
        h6 = card.h6.text
        info_dict[h6] = list()
        if card.table:
            rows_list = []
            table = card.table
            trs = table.find_all('tr')
            first_row_index = 0

            first_row = trs[0]
            first_row_tds = first_row.find_all("td", {"class": "tth"})
            if first_row_tds:
                headers = []
                for td in first_row_tds:
                    headers.append(td.text)
                first_row_index = 1

            for tr in trs[first_row_index:]:
                tds = [td.text for td in tr.find_all("td")]
                if first_row_index == 1:
                    rows_list.append(dict(zip(headers, tds)))
                elif first_row_index == 0:
                    if len(tds) == 2:
                        rows_list.append({tds[0]: tds[1]})
                    elif len(tds) > 2:
                        rows_list.append({tds[0]: tds[1:]})
                    else:
                        rows_list.append(tds[0])
            info_dict[h6].append(rows_list)

        ps = card.find_all('p')
        ps_dict = dict()
        for p in ps:
            if p.i:
                data_key = p.i.text.strip()
                data_value = p.text.replace(p.i.text, '').strip()

                if data_value:
                    ps_dict[data_key] = data_value
        if ps_dict:
            info_dict[h6].append(ps_dict)
    return info_dict


class ListOrg:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type] if data_type else self.get_input_data_type()

    def get_input_data_type(self):
        return set(Recognizer(self.input_data).get_data_types_list()).intersection(DATA_TYPES.keys())

    def get_lists_of_orgs(self):
        lists_of_orgs = []
        for data_type in self.data_type:
            urls = get_search_urls(data_type, self.input_data)
            for url in urls:
                lists_of_orgs.extend(get_paragraphs(url))
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
            complex_data.append(get_company_info(result['url']))

        return complex_data


def main():
    a = get_company_info("https://www.list-org.com/company/5308358")
    print(a)


if __name__ == "__main__":
    main()
