from bs4 import BeautifulSoup as bSoup
import requests

from pyosint.core.constants.headers import UA


def get_csrf_soup(base_url: str):
    return bSoup(requests.Session().get(base_url).content, features="html.parser")


def get_csrf_token(csrf_soup_data: bSoup):
    return csrf_soup_data.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']


def get_posted_data(base_url: str, raw_data: dict, csrf: str):
    headers_: dict = {'Referer': base_url, 'User-Agent': UA}
    data: dict = {'csrfmiddlewaretoken': csrf}
    data.update(raw_data)
    cookies: dict = {'csrftoken': csrf}
    return requests.Session().post(base_url, cookies=cookies, data=data, headers=headers_).content


def get_csrf_site_content(url: str, input_data: dict) -> bSoup:
    csrf_soup: bSoup = get_csrf_soup(url)
    csrf_token: str = get_csrf_token(csrf_soup)
    return bSoup(get_posted_data(url, input_data, csrf_token), features="html.parser")