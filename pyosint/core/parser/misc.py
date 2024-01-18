from bs4 import BeautifulSoup as bSoup

from pyosint.core.parser.text_cleaner import get_element_text
from pyosint.core.parser.middleware_parser import get_all_elements_from_parent
from pyosint.core.parser.table_handler import parse_table


def clean_attr(attr: str, attr_type: str) -> str:
    if attr_type == "key":
        if attr.endswith(":"):
            return attr[:-1]
    elif attr_type == "value":
        if attr.startswith(": "):
            return attr[2:]
    return attr


def get_text_from_ps(ps: list, clean_value: bool = False, clean_key: bool = False) -> dict:
    ps_dict: dict = dict()
    for p in ps:
        if p.i:
            data_key: str = p.i.text.strip()
            data_value: str = p.text.replace(p.i.text, '').strip()

            if data_value:
                if clean_value:
                    data_value = clean_attr(data_value, 'value')
                if clean_key:
                    data_key = clean_attr(data_key, 'key')
                ps_dict[data_key] = data_value
    return ps_dict


def get_table_dict(parsed: bSoup, headers: str = None) -> dict:
    info_dict: dict = dict()
    tables: list = get_all_elements_from_parent(parsed, 'table')
    if headers:
        tables_names: list = get_element_text(get_all_elements_from_parent(parsed, headers))
    else:
        tables_names: list = [None] * len(tables)
    for table, table_name in zip(tables, tables_names):
        trs: list = get_all_elements_from_parent(table, 'tr')
        rows_dict: dict = parse_table(trs, collection_type='dict')
        if rows_dict:
            if table_name:
                info_dict[table_name] = rows_dict
            else:
                info_dict.update(rows_dict)
    return info_dict


def remove_null_dict_values(org: dict) -> dict:
    for key, value in list(org.items()):
        if isinstance(value, dict):
            remove_null_dict_values(value)
            if not value:
                del org[key]
        elif value is None:
            del org[key]
    return org
