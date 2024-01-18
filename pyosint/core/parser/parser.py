from bs4 import BeautifulSoup as bSoup

from pyosint.core.parser.csrf_parser import get_csrf_site_content
from pyosint.core.parser.flattener import flatten_card_data
from pyosint.core.parser.text_cleaner import get_element_text, parse_strings_list
from pyosint.core.parser.requester import make_request
from pyosint.core.parser.middleware_parser import get_soup_from_raw, get_all_elements_from_parent, get_request_content
from pyosint.core.parser.misc import clean_attr, get_text_from_ps, get_table_dict, remove_null_dict_values
from pyosint.core.parser.table_handler import get_cells_data, parse_table
from pyosint.core.parser.concurrenter import process_requests_concurrently


class Parser:

    # concurrent
    @staticmethod
    def process_requests_concurrently(func, reqs=None, while_mode=False):
        return process_requests_concurrently(func, reqs, while_mode)

    # csrf parsing
    @staticmethod
    def get_csrf_site_content(url: str, input_data: dict) -> bSoup:
        return get_csrf_site_content(url, input_data)

    # flattening
    @staticmethod
    def flatten_card_data(card_data: dict | list | str, pass_empty=False) -> dict | list:
        return flatten_card_data(card_data, pass_empty)

    @staticmethod
    def parse_strings_list(find_all_headers_element):
        return parse_strings_list(find_all_headers_element)

    # middleware parsing
    @staticmethod
    def get_soup_from_raw(content) -> bSoup:
        return get_soup_from_raw(content)

    @staticmethod
    def get_all_elements_from_parent(parent_element, element: str, attributes: dict = None,
                                     recursive=True) -> list | None:
        return get_all_elements_from_parent(parent_element, element, attributes, recursive)

    @staticmethod
    def get_request_content(request_body):
        return get_request_content(request_body)

    # misc
    @staticmethod
    def clean_attr(attr: str, attr_type: str) -> str:
        return clean_attr(attr, attr_type)

    @staticmethod
    def get_text_from_ps(ps: list, clean_value: bool = False, clean_key: bool = False) -> dict:
        return get_text_from_ps(ps, clean_value, clean_key)

    @staticmethod
    def get_table_dict(parsed: bSoup, headers: str = None) -> dict:
        return get_table_dict(parsed, headers)

    @staticmethod
    def remove_null_dict_values(org: dict) -> dict:
        return remove_null_dict_values(org)

    # requesting
    @staticmethod
    def make_request(type_: str, url_: str, cookies_: dict = None, data_: dict = None, new_headers: dict = None,
                     use_default_headers: bool = True):
        return make_request(type_, url_, cookies_, data_, new_headers, use_default_headers)

    # table handling
    @staticmethod
    def get_cells_data(first_row_index: int, headers: list, tds: list, do_list: bool = False) -> list | dict | None:
        return get_cells_data(first_row_index, headers, tds, do_list)

    @staticmethod
    def parse_table(trs: list, collection_type: str = 'list', first_row_index: int = 0, headers: list = None,
                    do_list: bool = False, tds_ready: bool = False) -> list | dict:
        return parse_table(trs, collection_type, first_row_index, headers, do_list, tds_ready)

    # text cleaning
    @staticmethod
    def get_element_text(element) -> list | str:
        return get_element_text(element)
