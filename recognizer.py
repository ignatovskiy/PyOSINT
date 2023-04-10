import re


class Recognizer:
    def __init__(self, input_data):
        self.input_data = input_data

    def is_email(self):
        return bool(re.search(r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$", self.input_data))

    def is_phone(self):
        return bool(re.search(r"^[\+\(]?[1-9][0-9 .\-\(\)]{0,}[0-9\(\)]$", self.input_data))

    def is_ip(self):
        return bool(re.search(r"^(\b(\d{1,3}\.){3}(\d{1,3})\b)|([A-Fa-f0-9]{4}:){7}([A-Fa-f0-9]{4})$", self.input_data))

    def is_hostname(self):
        return bool(re.search(r"^(https?:\/\/)?(([A-Za-zА-Яа-я0-9\-])+\.)+([A-Za-zА-Яа-я0-9]+)$", self.input_data))

    def is_name(self):
        return bool(re.search(r"^([A-Za-zА-Яа-я]+ )+([A-Za-zА-Яа-я]+)$", self.input_data))

    def is_nickname(self):
        return bool(re.search(r"^[\w!@\$%#&\-\?<>~]+$", self.input_data))

    def is_address(self):
        return bool(re.search(r"^[а-яА-ЯёЁa-zA-Z0-9\s\.,\-/#№()&\'\"]+$", self.input_data))

    def is_company_name(self):
        return bool(re.search(r"^[а-яА-ЯёЁa-zA-Z\s\d&\(\)\[\]\.,\-\'\"/]+$", self.input_data))

    def get_data_type(self):
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
