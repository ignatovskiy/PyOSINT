from abc import abstractmethod

from bs4 import BeautifulSoup

from pyosint.core.parser.parser import Parser


class Company(Parser):

    @abstractmethod
    def get_lists_of_orgs(self) -> dict:
        pass

    @abstractmethod
    def get_search_results(self) -> list:
        pass

    @abstractmethod
    def get_complex_data(self) -> list:
        pass

    @abstractmethod
    def get_parsed_object(self, url) -> BeautifulSoup:
        pass

    @abstractmethod
    def get_search_url(self, input_data) -> str:
        pass

    @abstractmethod
    def get_company_info(self, url) -> dict:
        pass
