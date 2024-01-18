from bs4 import BeautifulSoup as bSoup


def get_soup_from_raw(content) -> bSoup:
    return bSoup(content, features="html.parser")


def get_all_elements_from_parent(parent_element, element: str, attributes: dict = None,
                                 recursive=True) -> list | None:
    try:
        return parent_element.find_all(element, attributes, recursive=recursive)
    except AttributeError:
        return None


def get_request_content(request_body):
    return request_body.content
