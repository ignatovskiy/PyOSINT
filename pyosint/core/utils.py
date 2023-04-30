from bs4 import BeautifulSoup as soup


def clean_attr(attr, attr_type):
    if attr_type == "key":
        if attr.endswith(":"):
            return attr[:-1]
    elif attr_type == "value":
        if attr.startswith(": "):
            return attr[2:]
    return attr


def get_text_from_ps(ps, clean_value=False, clean_key=False):
    ps_dict = dict()
    for p in ps:
        if p.i:
            data_key = p.i.text.strip()
            data_value = p.text.replace(p.i.text, '').strip()

            if data_value:
                if clean_value:
                    data_value = clean_attr(data_value, 'value')
                if clean_key:
                    data_key = clean_attr(data_key, 'key')
                ps_dict[data_key] = data_value
    return ps_dict


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


def get_table_dict(parsed, headers=None):
    info_dict = dict()
    tables = parsed.get_all_elements('table')
    if headers:
        tables_names = get_element_text(parsed.get_all_elements(headers))
    else:
        tables_names = [None] * len(tables)
    for table, table_name in zip(tables, tables_names):
        trs = parsed.get_all_elements('tr', parent_element=table)
        rows_dict = parse_table(trs, parsed, collection_type='dict')
        if rows_dict:
            if table_name:
                info_dict[table_name] = rows_dict
            else:
                info_dict.update(rows_dict)
    return info_dict


def parse_table(trs, parsed, collection_type='list', first_row_index=0, headers=None):
    if collection_type == "list":
        rows_collection = []
    elif collection_type == "dict":
        rows_collection = dict()
    else:
        rows_collection = None

    for tr in trs:
        tds_list = parsed.get_all_elements('td', parent_element=tr)
        tds_text_list = get_element_text(tds_list, sep_text=True)
        row_dict_element = get_cells_data(first_row_index, headers, tds_text_list)
        if row_dict_element:
            if collection_type == "dict":
                rows_collection.update(row_dict_element)
            elif collection_type == "list":
                rows_collection.append(row_dict_element)
    return rows_collection


def remove_null_dict_values(org):
    for key, value in list(org.items()):
        if isinstance(value, dict):
            remove_null_dict_values(value)
            if not value:
                del org[key]
        elif value is None:
            del org[key]
    return org


def get_element_text(element, sep_text=False):
    if isinstance(element, list):
        if sep_text:
            return [el.get_text(separator='. ', strip=True)
                    .replace("\xa0", ' ').replace("\u2009", ' ').replace('\n', '')
                    for el in element]
        else:
            return [el.text.replace("\xa0", ' ') for el in element]
    else:
        if sep_text:
            return element.get_text(separator='. ', strip=True) \
                .replace("\xa0", ' ').replace("\u2009", ' ').replace('\n', '')
        else:
            return element.text.replace("\xa0", ' ')


def get_soup_from_raw(content):
    return soup(content, features="html.parser")


def get_all_elements_from_parent(parent_element, element: str, attributes: dict = None, recursive=True) -> list|None:
    try:
        return parent_element.find_all(element, attributes, recursive=recursive)
    except AttributeError:
        return None
