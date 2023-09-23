from abc import abstractmethod

from pyosint.core.parser import Parser


class Company(Parser):

    @abstractmethod
    def get_lists_of_orgs(self):
        pass

    @abstractmethod
    def get_search_results(self):
        pass

    @abstractmethod
    def get_complex_data(self):
        pass

    @abstractmethod
    def get_parsed_object(self, url):
        pass

    @abstractmethod
    def get_search_url(self, input_data):
        pass

    @abstractmethod
    def get_company_info(self, url):
        pass