import requests

from pyosint.core.constants.headers import UA


def get_request(url, cookies=None, data=None, headers=None):
    return requests.get(url, cookies=cookies, data=data, headers=headers)


def post_request(url, cookies=None, data=None, headers=None):
    return requests.post(url, cookies=cookies, data=data, headers=headers)


def make_request(type_: str, url_: str, cookies_: dict = None, data_: dict = None, new_headers: dict = None,
                 use_default_headers: bool = True):
    if use_default_headers:
        headers_ = {"User-Agent": UA}
    else:
        headers_ = dict()
    if new_headers:
        headers_.update(new_headers)
    if not headers_:
        headers_ = None

    if type_ == "get":
        return get_request(url_, cookies=cookies_, data=data_, headers=headers_)
    elif type_ == "post":
        return post_request(url_, cookies=cookies_, data=data_, headers=headers_)
