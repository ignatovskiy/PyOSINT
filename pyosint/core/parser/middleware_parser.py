import json

from bs4 import BeautifulSoup as bSoup


def get_soup_from_raw(content) -> bSoup:
    return bSoup(content, features='lxml', parser='lxml')


def get_all_elements_from_parent(parent_element, element: str, attributes: dict = None,
                                 recursive=True) -> list | None:
    try:
        return parent_element.find_all(element, attributes, recursive=recursive)
    except AttributeError:
        return None


def get_request_content(request_body, return_json=False):
    if return_json:
        try:
            return request_body.json()
        except json.decoder.JSONDecodeError:
            return json.loads(request_body.text)
    else:
        return request_body.content
