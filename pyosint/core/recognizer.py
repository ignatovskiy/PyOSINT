import ipaddress
import re

import pyosint.core.constants as constants


def exclude_types(types_list):
    for type_ in types_list:
        if type_ in constants.EXCLUDE_TYPES:
            return [type_]
    return types_list


class Recognizer:
    def __init__(self, input_data: str):
        self.input_data: str = input_data

    def is_email(self) -> bool:
        return bool(re.search(constants.EMAIL_REGEXP, self.input_data))

    def is_phone(self) -> bool:
        return bool(re.search(constants.PHONE_REGEXP, self.input_data))

    def is_ip(self) -> bool:
        if bool(re.search(constants.IP_REGEXP, self.input_data)):
            try:
                ipaddress.ip_address(self.input_data)
                return True
            except ValueError:
                return False
        else:
            return False

    def is_hostname(self) -> bool:
        return bool(re.search(constants.HOST_REGEXP, self.input_data))

    def is_name(self):
        return bool(re.search(constants.NAME_REGEXP, self.input_data))

    def is_nickname(self) -> bool:
        return bool(re.search(constants.NICK_REGEXP, self.input_data))

    def is_address(self) -> bool:
        return bool(re.search(constants.ADDRESS_REGEXP, self.input_data))

    def is_company_name(self) -> bool:
        return bool(re.search(constants.COMPANY_REGEXP, self.input_data))

    def is_id(self) -> bool:
        return bool(re.search(constants.ID_REGEXP, self.input_data))

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
            "id": self.is_id()
        }

    def get_data_types_list(self) -> list:
        return exclude_types([key for key, value in self.get_data_types_dict().items() if value])

    def get_categories(self) -> list:
        categories = list()
        types = set(self.get_data_types_list())
        for key, value in constants.CATEGORIES.items():
            if value.intersection(types):
                categories.append(key)
        return categories
