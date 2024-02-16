from pyosint.core.constants.symbols import PHONE, HOSTNAME, ID


def fix_data(data: str, symbols: list) -> str:
    for symbol in symbols:
        data = data.replace(symbol, '')
    return data


class Converter:
    def __init__(self, input_data: str, type_: str):
        self.input_data: str = input_data
        self.type: str = type_
        self.conversion_dict: dict = {
            "email": self.convert_email(),
            "phone": self.convert_phone(),
            "ip": self.convert_ip(),
            "hostname": self.convert_hostname(),
            "name": self.convert_name(),
            "nickname": self.convert_nickname(),
            "address": self.convert_address(),
            "company": self.convert_company_name(),
            "id": self.convert_id(),
            "filename": self.convert_filename()
        }

    def convert_email(self) -> str:
        return self.input_data.lower()

    def convert_phone(self) -> str:
        phone: str = self.input_data
        return fix_data(phone, PHONE)

    def convert_ip(self) -> str:
        return self.input_data

    def convert_hostname(self) -> str:
        hostname: str = self.input_data
        return fix_data(hostname, HOSTNAME)

    def convert_name(self) -> str:
        return self.input_data

    def convert_nickname(self) -> str:
        return self.input_data.lower()

    def convert_address(self) -> str:
        return self.input_data

    def convert_company_name(self) -> str:
        return self.input_data

    def convert_filename(self) -> str:
        return self.input_data

    def convert_id(self) -> str:
        id_: str = self.input_data
        return fix_data(id_, ID)

    def get_converted_data(self) -> str:
        return self.conversion_dict[self.type]
