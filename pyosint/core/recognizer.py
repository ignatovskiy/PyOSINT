import ipaddress
import re

import pyosint.core.constants.exclusions as exclusions
import pyosint.core.constants.regexps as regexps
import pyosint.core.constants.categories as categories


def exclude_types(types_list: list) -> list:
    for priority_type in exclusions.EXCLUDE_TYPES:
        for type_ in types_list:
            if type_ == priority_type:
                return [type_]
    return types_list


class Recognizer:
    def __init__(self, input_data: str):
        self.input_data: str = input_data

    def is_email(self) -> bool:
        return bool(re.search(regexps.EMAIL, self.input_data))

    def is_phone(self) -> bool:
        return bool(re.search(regexps.PHONE, self.input_data))

    def is_ip(self) -> bool:
        if bool(re.search(regexps.IP, self.input_data)):
            try:
                ipaddress.ip_address(self.input_data)
                return True
            except ValueError:
                return False
        else:
            return False

    def is_hostname(self) -> bool:
        return bool(re.search(regexps.HOST, self.input_data))

    def is_name(self) -> bool:
        return bool(re.search(regexps.NAME, self.input_data))

    def is_nickname(self) -> bool:
        return bool(re.search(regexps.NICK, self.input_data))

    def is_address(self) -> bool:
        return bool(re.search(regexps.ADDRESS, self.input_data))

    def is_company_name(self) -> bool:
        return bool(re.search(regexps.COMPANY, self.input_data))

    def is_filename(self) -> bool:
        return bool(re.search(regexps.FILENAME, self.input_data))

    def is_id(self) -> bool:
        return bool(re.search(regexps.ID, self.input_data))

    def get_data_types_dict(self) -> dict:
        return {
            "email": self.is_email(),
            "phone": self.is_phone(),
            "ip": self.is_ip(),
            "hostname": self.is_hostname(),
            "name": self.is_name(),
            "nickname": self.is_nickname(),
            "address": self.is_address(),
            "company": self.is_company_name(),
            "id": self.is_id(),
            "filename": self.is_filename()
        }

    def get_data_types_list(self) -> list:
        return [key for key, value in self.get_data_types_dict().items() if value]

    def get_categories(self) -> list:
        categories_list: list = list()
        types: set = set(self.get_data_types_list())
        for key, value in categories.CATEGORIES.items():
            if value.intersection(types):
                categories_list.append(key)
        return categories_list
