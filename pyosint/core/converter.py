class Converter:
    def __init__(self, input_data, type_):
        self.input_data = input_data
        self.type = type_
        self.conversion_dict = {
            "email": self.convert_email(),
            "phone": self.convert_phone(),
            "ip": self.convert_ip(),
            "hostname": self.convert_hostname(),
            "name": self.convert_name(),
            "nickname": self.convert_nickname(),
            "address": self.convert_address(),
            "company": self.convert_company_name(),
            "id": self.convert_id()
        }

    def convert_email(self):
        return self.input_data.lower()

    def convert_phone(self):
        phone: str = self.input_data
        phone_symbols = ['-', '(', ')', ' ', '.', '+']
        for symbol in phone_symbols:
            phone = phone.replace(symbol, '')
        return phone

    def convert_ip(self):
        return self.input_data

    def convert_hostname(self):
        hostname: str = self.input_data
        hostname_symbols = ['https://', 'http://']
        for symbol in hostname_symbols:
            hostname = hostname.replace(symbol, '')
        return hostname

    def convert_name(self):
        return self.input_data

    def convert_nickname(self):
        return self.input_data.lower()

    def convert_address(self):
        return self.input_data

    def convert_company_name(self):
        return self.input_data

    def convert_id(self):
        id_: str = self.input_data
        id_symbols = ['-', ' ']
        for symbol in id_symbols:
            id_ = id_.replace(symbol, '')
        return id_

    def get_converted_data(self):
        return self.conversion_dict[self.type]
