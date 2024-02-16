from pyosint.core.parser.flattener import flatten_card_data
from pyosint.core.parser.text_cleaner import get_element_text, parse_strings_list
from pyosint.core.parser.middleware_parser import get_all_elements_from_parent


def flatten_row(input_list):
    result = []

    for item in input_list:
        if isinstance(item, list):
            result.extend(flatten_row(item))
        else:
            result.append(item)
    return result


def init_row_collection(collection_type):
    if collection_type == 'dict':
        return {}
    elif collection_type == 'list':
        return []
    return None


def handle_row_collection(rows_collection, row_dict_element, collection_type):
    if row_dict_element:
        if collection_type == "dict":
            if not isinstance(row_dict_element, dict):
                rows_collection.update({'': row_dict_element})
            else:
                rows_collection.update(row_dict_element)
        elif collection_type == "list":
            rows_collection.append(row_dict_element)
    return rows_collection


def get_cells_data(first_row_index: int, headers: list, tds: list, do_list: bool = False, list_of_lists: bool = False)\
        -> list | dict | None:
    if not isinstance(tds, list):
        return tds
    if list_of_lists and len(tds) >= 1:
        return {sublist[0]: sublist[1:] for sublist in tds if isinstance(sublist, list)}
    if first_row_index >= 1 and len(headers) == len(tds):
        return dict(zip(headers, tds))
    elif first_row_index == 0:
        if len(tds) == 2:
            temp_key = tds[0][0] if isinstance(tds[0], list) and len(tds[0]) == 1 else tds[0]
            if isinstance(tds[0], list):
                return tds
            return {temp_key: tds[1]}
        elif len(tds) > 2:
            temp_list = flatten_row(tds)
            if do_list:
                return temp_list
            else:
                if temp_list[0] != '':
                    if isinstance(temp_list[0], str):
                        return {temp_list[0]: temp_list[1:]}
                    else:
                        if isinstance(temp_list[1], str):
                            return {temp_list[1]: [temp_list[0]] + temp_list[2:]}
                        else:
                            return temp_list
                else:
                    return {temp_list[1]: temp_list[2:]}
        elif len(tds) == 1:
            return tds[0]
    return None


def parse_table(trs: list, collection_type: str = 'list', first_row_index: int = 0, headers: list = None,
                do_list: bool = False, tds_ready: bool = False) -> list | dict:
    rows_collection = init_row_collection(collection_type)

    if headers:
        headers = [el[0] if isinstance(el, list) else el for el in parse_strings_list(headers)]

    for tr in trs:
        if not tds_ready:
            tds_list = get_all_elements_from_parent(tr, 'td')

            if not tds_list:
                if not headers:
                    headers = get_element_text(get_all_elements_from_parent(tr, 'th'))
                continue

            tds_text_list = parse_strings_list(tds_list)
            if isinstance(tds_text_list, str):
                tds_text_list = [tds_text_list]
        else:
            tds_text_list = trs

        if headers and len(tds_text_list) > len(headers):
            tds_text_list = flatten_card_data(tds_text_list)

        row_dict_element = get_cells_data(first_row_index, headers, tds_text_list, do_list)

        rows_collection = handle_row_collection(rows_collection, row_dict_element, collection_type)

        if tds_ready:
            break
    return flatten_card_data(rows_collection)
