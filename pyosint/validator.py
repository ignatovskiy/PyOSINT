import ipaddress


class Validator:
    def __init__(self, input_data: str, types_dict: dict):
        self.input_data: str = input_data
        self.types_dict: dict = types_dict
        self.validator_dict: dict = {
            "ip": self.validate_ip,
            "name": self.validate_name,
            "phone": self.validate_phone,
            "hostname": self.validate_hostname,
            "address": self.validate_address,
            "company": self.validate_company,
            "email": self.validate_email,
            "nickname": self.validate_nickname
        }

    def validate_ip(self):
        try:
            ipaddress.ip_address(self.input_data)
            return True
        except ValueError:
            return False

    def validate_name(self):
        return True

    def validate_phone(self):
        return True

    def validate_hostname(self):
        return True

    def validate_address(self):
        return True

    def validate_company(self):
        return True

    def validate_email(self):
        return True

    def validate_nickname(self):
        return True

    def validate_types(self) -> list:
        validated_list: list = list()
        for key in self.types_dict.keys():
            if self.types_dict[key]:
                validator_func = self.validator_dict[key]
                if validator_func():
                    validated_list.append(key)
        return validated_list
