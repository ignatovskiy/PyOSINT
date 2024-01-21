def combine_dicts_if_unique_keys(dict_list):
    if all(len(d) == 1 for d in dict_list):
        keys = [list(d.keys())[0] for d in dict_list]
        if len(set(keys)) == len(dict_list):
            combined_dict = {key: value for d in dict_list for key, value in d.items()}
            return combined_dict
        else:
            combined_dict = {}
            for d in dict_list:
                for key, value in d.items():
                    if key in combined_dict:
                        if (isinstance(combined_dict[key], (dict, str))
                                or (isinstance(combined_dict[key], list)
                                    and all(isinstance(item, (dict, str)) for item in combined_dict[key]))):
                            combined_dict[key] = [combined_dict[key]]
                        combined_dict[key].append(value)
                    else:
                        combined_dict[key] = value
            return combined_dict
    return dict_list


def flatten_dict_pair(key, value, pass_empty):
    temp_key, temp_value = key, value
    if isinstance(value, str) and value == '':
        temp_value = None
        return temp_key, temp_value
    if isinstance(key, list) and len(key) == 1:
        temp_key = key[0]
    if isinstance(value, list):
        temp_value = flatten_list(temp_value, pass_empty)
    elif isinstance(value, dict):
        temp_value = flatten_dict(temp_value, pass_empty)
    return temp_key, temp_value


def flatten_dict(unflatten_dict, pass_empty):
    card_dict = {}
    for key, value in unflatten_dict.items():
        temp_key, temp_value = flatten_dict_pair(key, value, pass_empty)
        if temp_value:
            card_dict[temp_key] = temp_value
    return card_dict


def flatten_list_el(list_el, pass_empty):
    if isinstance(list_el, str):
        return list_el
    elif isinstance(list_el, list):
        return flatten_list(list_el, pass_empty)
    elif isinstance(list_el, dict):
        return flatten_dict(list_el, pass_empty)
    return list_el


def transform_list_to_dict(raw_list):
    result = [{}]
    current_key = None

    if isinstance(raw_list, list):
        for item in raw_list:
            if isinstance(item, str) and item.endswith(":"):
                temp_key = item.strip(":")
                if current_key != temp_key:
                    current_key = temp_key
                    result[0][current_key] = []
            else:
                if current_key is not None:
                    result[0][current_key].append(item)
                else:
                    result.append(item)
        if isinstance(result[0], dict) and not result[0]:
            result.pop(0)
        return result
    else:
        return raw_list


def flatten_list(unflatten_list, pass_empty):
    temp_list = [flatten_list_el(el, pass_empty) for el in unflatten_list if pass_empty or el]
    if temp_list:
        if len(temp_list) == 1:
            temp_list = temp_list[0]
        elif all(isinstance(item, dict) for item in temp_list):
            temp_list = combine_dicts_if_unique_keys(temp_list)
    else:
        return ''
    return transform_list_to_dict(temp_list)


def flatten_card_data(card_data: dict | list | str, pass_empty=False) -> dict | list:
    if isinstance(card_data, list):
        return flatten_list(card_data, pass_empty)
    elif isinstance(card_data, dict):
        return flatten_dict(card_data, pass_empty)
    return card_data
