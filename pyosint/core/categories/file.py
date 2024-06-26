from abc import abstractmethod

from bs4 import BeautifulSoup

from pyosint.core.parser.parser import Parser


class File(Parser):

    @abstractmethod
    def get_search_url(self, *args) -> str:
        pass

    @abstractmethod
    def get_complex_data(self) -> list:
        pass

    @abstractmethod
    def get_parsed_object(self, *args) -> BeautifulSoup | dict | bytes:
        pass
