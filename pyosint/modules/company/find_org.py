from pyosint.core.parser import Parser
from pyosint.core.recognizer import Recognizer


import re


URL = "http://www.find-org.com"

LOCATION_NAME_PATTERN = r'\(([^,]+)'
OGRN_PATTERN = r',\s*ОГРН:\s*([^\s,]+)'
INN_PATERN = r',\s*ИНН:\s*([^\s,)]+)([,)]\s*.*|$)'

NAME = 'name'
INN = 'inn'
OGRN = 'ogrn'
OKPO = 'okpo'
ADDRESS = 'address'
HEAD = 'chief'
PHONE = 'phone'

DATA_TYPES = {
    'company': [NAME],
    'id': [INN, OGRN, OKPO],
    'address': [ADDRESS],
    'name': [HEAD],
    'phone': [PHONE]
}


def get_search_url(data_type, input_data):
    return f"{URL}/search/{data_type}/?val={input_data}"


def get_search_urls(data_type, input_data):
    urls_list = []
    for type_ in DATA_TYPES[data_type]:
        urls_list.append(get_search_url(type_, input_data))
    return urls_list


def get_paragraphs(url):
    return Parser(url, 'get').get_all_elements('p')


def get_company_info(url):
    info_dict = dict()
    data_list = get_paragraphs(url)
    for el in data_list:
        if el.i:
            data_key = el.i.text.strip()
            data_value = el.text.replace(el.i.text, '').strip()

            if data_value:
                info_dict[data_key] = data_value
    return info_dict


class FindOrg:
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
            link_data = org.a
            span_data = org.span.text

            company_name = link_data.text
            company_link = link_data.get('href')

            span_data_list = span_data.split(',')
            company_address, company_ogrn, company_inn = span_data_list[:3]
            company_address = company_address.strip().replace('(', '').replace(')', '')
            company_ogrn = company_ogrn.strip().replace("ОГРН: ", '')
            company_inn = company_inn.strip().replace(')', '').replace("ИНН: ", '')
            company_active = False if "недействующее" in str(span_data) else True

            results.append({
                "company": company_name,
                "address": company_address,
                "id_ogrn": company_ogrn,
                "id_inn": company_inn,
                "id_is_active": company_active,
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
    pass


if __name__ == "__main__":
    main()
