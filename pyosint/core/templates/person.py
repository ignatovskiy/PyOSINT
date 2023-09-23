from abc import abstractmethod

from pyosint.core.parser import Parser


class Person(Parser):

    @abstractmethod
    def get_search_url(self, input_data):
        pass

    @abstractmethod
    def get_complex_data(self):
        pass

    @abstractmethod
    def get_parsed_object(self, url):
        pass