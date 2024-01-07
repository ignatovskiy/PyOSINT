import requests
from bs4 import BeautifulSoup as bSoup

from pyosint.core.constants.headers import UA


class Parser:

    @staticmethod
    def clean_attr(attr: str, attr_type: str) -> str:
        if attr_type == "key":
            if attr.endswith(":"):
                return attr[:-1]
        elif attr_type == "value":
            if attr.startswith(": "):
                return attr[2:]
        return attr

    def get_text_from_ps(self, ps: list, clean_value: bool = False, clean_key: bool = False) -> dict:
        ps_dict: dict = dict()
        for p in ps:
            if p.i:
                data_key: str = p.i.text.strip()
                data_value: str = p.text.replace(p.i.text, '').strip()

                if data_value:
                    if clean_value:
                        data_value = self.clean_attr(data_value, 'value')
                    if clean_key:
                        data_key = self.clean_attr(data_key, 'key')
                    ps_dict[data_key] = data_value
        return ps_dict

    @staticmethod
    def flatten_card_data(card_data: dict | list) -> dict | list:
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
    def get_cells_data(first_row_index: int, headers: list, tds: list, do_list: bool = False) -> list | dict | None:
        if first_row_index >= 1:
            if len(headers) == len(tds):
                return dict(zip(headers, tds))
            else:
                return None
        elif first_row_index == 0:
            if len(tds) == 2:
                return {tds[0]: tds[1]}
            elif len(tds) > 2:
                if do_list:
                    return tds
                else:
                    return {tds[0]: tds[1:]}
            elif len(tds) == 1:
                return tds[0]

    def get_table_dict(self, parsed: bSoup, headers: str = None) -> dict:
        info_dict: dict = dict()
        tables: list = self.get_all_elements_from_parent(parsed, 'table')
        if headers:
            tables_names: list = self.get_element_text(self.get_all_elements_from_parent(parsed, headers))
        else:
            tables_names: list = [None] * len(tables)
        for table, table_name in zip(tables, tables_names):
            trs: list = self.get_all_elements_from_parent(table, 'tr')
            rows_dict: dict = self.parse_table(trs, collection_type='dict')
            if rows_dict:
                if table_name:
                    info_dict[table_name] = rows_dict
                else:
                    info_dict.update(rows_dict)
        return info_dict

    def parse_table(self, trs: list, collection_type: str = 'list', first_row_index: int = 0, headers: list = None,
                    do_list: bool = False, sep_text: bool = True, th_key: bool = False) -> list | dict:
        rows_collection: None = None
        if collection_type == "list":
            rows_collection: list = []
        elif collection_type == "dict":
            rows_collection: dict = dict()

        for tr in trs:
            tds_list: list = self.get_all_elements_from_parent(tr, 'td')
            tds_text_list: list = self.get_element_text(tds_list, sep_text=sep_text)
            if th_key:
                headers: list = self.get_element_text(self.get_all_elements_from_parent(tr, 'th'))
                if not headers:
                    continue
            row_dict_element: list | dict | None = self.get_cells_data(first_row_index, headers, tds_text_list, do_list)
            if row_dict_element:
                if collection_type == "dict":
                    try:
                        rows_collection.update(row_dict_element)
                    except ValueError:
                        if rows_collection.get("Остальное"):
                            rows_collection["Остальное"].append(row_dict_element)
                        else:
                            rows_collection["Остальное"] = list()
                elif collection_type == "list":
                    rows_collection.append(row_dict_element)
        return rows_collection

    def remove_null_dict_values(self, org: dict) -> dict:
        for key, value in list(org.items()):
            if isinstance(value, dict):
                self.remove_null_dict_values(value)
                if not value:
                    del org[key]
            elif value is None:
                del org[key]
        return org

    @staticmethod
    def get_element_text(element, sep_text=False) -> list | str:
        if isinstance(element, list):
            if sep_text:
                return [el.get_text(separator='. ', strip=True)
                        .replace("\xa0", ' ').replace("\u2009", ' ').replace('\n', '')
                        for el in element if not isinstance(el, str)]
            else:
                return [el.text.replace("\xa0", ' ') for el in element if not isinstance(el, str)]
        else:
            if sep_text:
                return element.get_text(separator='. ', strip=True) \
                    .replace("\xa0", ' ').replace("\u2009", ' ').replace('\n', '')
            else:
                return element.text.replace("\xa0", ' ')

    @staticmethod
    def get_soup_from_raw(content) -> bSoup:
        return bSoup(content, features="html.parser")

    @staticmethod
    def get_all_elements_from_parent(parent_element, element: str, attributes: dict = None,
                                     recursive=True) -> list | None:
        try:
            return parent_element.find_all(element, attributes, recursive=recursive)
        except AttributeError:
            return None

    @staticmethod
    def make_request(type_: str, url_: str, cookies_: dict = None, data_: dict = None, new_headers: dict = None,
                     use_default_headers: bool = True):
        if use_default_headers:
            headers_ = {"User-Agent": UA}
        else:
            headers_ = dict()
        if new_headers:
            headers_.update(new_headers)
        if not headers_:
            headers_ = None

        def get_request(url, cookies=None, data=None, headers=None):
            return requests.get(url, cookies=cookies, data=data, headers=headers)

        def post_request(url, cookies=None, data=None, headers=None):
            return requests.post(url, cookies=cookies, data=data, headers=headers)

        if type_ == "get":
            return get_request(url_, cookies=cookies_, data=data_, headers=headers_)
        elif type_ == "post":
            return post_request(url_, cookies=cookies_, data=data_, headers=headers_)

    @staticmethod
    def get_request_content(request_body):
        return request_body.content

    @staticmethod
    def get_csrf_site_content(url: str, input_data: dict) -> bSoup:
        def get_csrf_soup(base_url: str):
            return bSoup(requests.Session().get(base_url).content, features="html.parser")

        def get_csrf_token(csrf_soup_data: bSoup):
            return csrf_soup_data.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']

        def get_posted_data(base_url: str, raw_data: dict, csrf: str):
            headers_: dict = {'Referer': base_url, 'User-Agent': UA}
            data: dict = {'csrfmiddlewaretoken': csrf}
            data.update(raw_data)
            cookies: dict = {'csrftoken': csrf}
            return requests.Session().post(url, cookies=cookies, data=data, headers=headers_).content

        csrf_soup: bSoup = get_csrf_soup(url)
        csrf_token: str = get_csrf_token(csrf_soup)
        return bSoup(get_posted_data(url, input_data, csrf_token), features="html.parser")
