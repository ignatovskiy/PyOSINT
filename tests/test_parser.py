import bs4
import requests

from pyosint.core.parser import Parser


def test_get_request():
    assert isinstance(Parser("https://google.com", 'get').make_request(), requests.Response)


def test_post_request():
    assert isinstance(Parser("https://google.com", 'post').make_request(), requests.Response)


def test_get_content():
    assert isinstance(Parser("https://google.com", 'get').get_content(), bytes)


def test_get_status_code():
    assert isinstance(Parser("https://google.com", 'get').get_status_code(), int)


def test_get_soup():
    assert isinstance(Parser("https://google.com", 'get').get_soup(), bs4.BeautifulSoup)


def test_get_all_elements():
    assert isinstance(Parser("https://google.com", 'get').get_all_elements('a'), list)


def test_get_all_attrs_values():
    assert isinstance(Parser("https://google.com", 'get').get_all_attrs_values('a', 'href'), list)
