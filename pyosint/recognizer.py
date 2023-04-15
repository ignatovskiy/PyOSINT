import ipaddress
import re


EMAIL_REGEXP = r"^[A-Za-z0-9\._%\+\-]+@([A-Za-z0-9\-]+\.)+[A-Z|a-z]{2,}$"
PHONE_REGEXP = r"^[\+\(]?[1-9][0-9 .\-\(\)]{0,}[0-9\(\)]$"
IP_REGEXP = r"^((\b(\d{1,3}\.){3}(\d{1,3})\b)|([A-Fa-f0-9]{1,4}:{1,2}){1,7}([A-Fa-f0-9]{1,4}))$"
HOST_REGEXP = r"^(https?:\/\/)?(([A-Za-zА-Яа-я0-9\-])+\.)+([A-Za-zА-Яа-я0-9]+)$"
NAME_REGEXP = r"^([A-Za-zА-Яа-я]+ )+([A-Za-zА-Яа-я]+)$"
NICK_REGEXP = r"^[\w!@\$%#&\-\?<>~]+$"
ADDRESS_REGEXP = r"^[а-яА-ЯёЁa-zA-Z0-9\s\.\,\-\/№\(\)&\'\"]+$"
COMPANY_REGEXP = r"^[а-яА-ЯёЁa-zA-Z\s\d&\(\)\[\]\.\,\-\'\"/]+$"

EXCLUDE_TYPES = ["ip", "email"]


def exclude_types(types_list):
    for type_ in types_list:
        if type_ in EXCLUDE_TYPES:
            return [type_]
    return types_list


class Recognizer:
    def __init__(self, input_data: str):
        self.input_data: str = input_data

    def is_email(self) -> bool:
        return bool(re.search(EMAIL_REGEXP, self.input_data))

    def is_phone(self) -> bool:
        return bool(re.search(PHONE_REGEXP, self.input_data))

    def is_ip(self) -> bool:
        return bool(re.search(IP_REGEXP, self.input_data))

    def is_hostname(self) -> bool:
        return bool(re.search(HOST_REGEXP, self.input_data))

    def is_name(self):
        return bool(re.search(NAME_REGEXP, self.input_data))

    def is_nickname(self) -> bool:
        return bool(re.search(NICK_REGEXP, self.input_data))

    def is_address(self) -> bool:
        return bool(re.search(ADDRESS_REGEXP, self.input_data))

    def is_company_name(self) -> bool:
        return bool(re.search(COMPANY_REGEXP, self.input_data))

    def get_data_types_dict(self) -> dict:
        return {
            "email": self.is_email(),
            "phone": self.is_phone(),
            "ip": self.is_ip(),
            "hostname": self.is_hostname(),
            "name": self.is_name(),
            "nickname": self.is_nickname(),
            "address": self.is_address(),
            "company": self.is_company_name()
        }

    def get_data_types_list(self) -> list:
        return exclude_types([key for key, value in self.get_data_types_dict().items() if value])
