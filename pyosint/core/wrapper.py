import importlib
import importlib.util
import os

from pyosint.core.recognizer import Recognizer
from pyosint.core.converter import Converter


EXCLUDE_MODULES = ["test.py", "__init__.py"]
EXCLUDE_NAMES = ["Recognizer", "soup"]


class Wrapper:
    def __init__(self, input_data: str, category: str = None):
        self.input_data: str = input_data
        self.category: str = category

    def get_categories(self):
        return [self.category] if self.category else Recognizer(self.input_data).get_categories()

    @staticmethod
    def get_modules_list(category):
        return [
            filename[:-3]
            for filename in os.listdir(f"pyosint/modules/{category}/")
            if filename.endswith(".py") and filename not in EXCLUDE_MODULES
        ]

    def get_modules_classes(self):
        classes = dict()
        modules_dict = self.import_modules()
        for category in modules_dict:
            classes[category] = list()
            for file in modules_dict[category]:
                spec = importlib.util.spec_from_file_location(file, os.path.join(f"pyosint/modules/{category}/", f"{file}.py"))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and name not in EXCLUDE_NAMES:
                        classes[category].append(obj)
        return classes

    def handle_parsers(self):
        classes_dict = self.get_modules_classes()
        data = dict()
        if len(classes_dict.keys()) == 1:
            types = Recognizer(self.input_data).get_data_types_list()
            if len(types) == 1:
                self.input_data = Converter(self.input_data, types[0]).get_converted_data()
        for category in classes_dict:
            for class_ in classes_dict[category]:
                temp_class = class_(self.input_data)
                temp_data = temp_class.get_complex_data()
                data[class_.__name__] = temp_data
        return data

    def import_modules(self):
        modules_dict = dict()
        categories = self.get_categories()
        for category in categories:
            modules_dict[category] = self.get_modules_list(category)
        return modules_dict


def main():
    pass


if __name__ == "__main__":
    main()
