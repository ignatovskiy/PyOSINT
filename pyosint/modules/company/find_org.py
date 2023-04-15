from pyosint.core.parser import Parser

URL = "http://www.find-org.com/search/name/?val="

NAME = 'name'
INN = 'inn'
OGRN = 'ogrn'
OKPO = 'okpo'
ADDRESS = 'address'
HEAD = 'chief'
PHONE = 'phone'


def get_search_url(data_type, input_data):
    return f"{URL}/{data_type}/?val={input_data}"


class FindOrg:
    def __init__(self, name=None, inn=None, ogrn=None, okpo=None, address=None, head=None, phone=None):
        self.name = name
        self.inn = inn
        self.ogrn = ogrn
        self.okpo = okpo
        self.address = address
        self.head = head
        self.phone = phone

    def get_list_of_orgs(self):
        Parser(URL, )


def main():
    pass


if __name__ == "__main__":
    main()
