import re

from pyosint.core.constants.removals import TRANSLATION_TABLE
from pyosint.core.parser.flattener import flatten_card_data


def remove_symbols(raw_element):
    return re.sub(r'\s{2,}',
                  ' ',
                  raw_element.translate(TRANSLATION_TABLE).strip())


def strip_text(temp_list):
    temp_stripped_list = [
        [item if isinstance(item, str) else [el for el in item if el]
         for item in sublist]
        for sublist in temp_list if sublist
    ]
    return flatten_card_data(temp_stripped_list)


def clean_text(temp_element):
    for br_tag in temp_element.find_all('br'):
        br_tag.replace_with('\n' * 10)

    temp_list = [remove_symbols(subel)
                 for subel in temp_element.get_text().split('\n' * 10)]

    return temp_list


def get_element_text(element) -> list | str:
    if isinstance(element, list):
        result_list = [clean_text(el) if not isinstance(el, str) else remove_symbols(el).strip() for el in element]
    else:
        result_list = clean_text(element) if not isinstance(element, str) else remove_symbols(element).strip()
    return strip_text(result_list)


def parse_strings_list(find_all_headers_element):
    return flatten_card_data(get_element_text(find_all_headers_element), pass_empty=True)
