import importlib
import importlib.util
import os
import concurrent.futures
from functools import partial

from pyosint.core.recognizer import Recognizer
from pyosint.core.converter import Converter
import pyosint.core.constants.exclusions as exclusions
from pyosint.core.logger import log


class Wrapper:
    def __init__(self, input_data: str, category: str = None):
        self.input_data: str = input_data
        self.category: str = category

    def get_categories(self) -> list:
        return [self.category] if self.category else Recognizer(self.input_data).get_categories()

    def get_modules_dict(self) -> dict:
        modules_dict: dict = dict()
        categories: list = self.get_categories()
        for category in categories:
            modules_dict[category] = self.get_modules_list(category)
        return modules_dict

    @staticmethod
    def get_modules_list(category: str) -> list:
        return [
            filename[:-3]
            for filename in os.listdir(f"pyosint/modules/{category}/")
            if filename.endswith(".py") and filename not in exclusions.EXCLUDE_MODULES
        ]

    @staticmethod
    def import_module(file: str, category: str):
        spec = importlib.util.spec_from_file_location(
            file,
            os.path.join(f"pyosint/modules/{category}/",
                         f"{file}.py"
                         ))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def import_modules(self, modules_dict: dict, category: str):
        modules = list()
        for file in modules_dict[category]:
            module = self.import_module(file, category)
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and name not in exclusions.EXCLUDE_NAMES:
                    modules.append(obj)
        return modules

    def get_modules_classes(self) -> dict:
        classes: dict = dict()
        modules_dict = self.get_modules_dict()
        for category in modules_dict:
            classes[category] = self.import_modules(modules_dict, category)
        return classes

    @staticmethod
    def process_class(category, class_, input_data, types):
        class_name = class_.__name__
        if class_name.lower() != category.lower():
            temp_class = class_(input_data)
            if set(types).intersection(set(temp_class.types)):
                log("info", f"Starting {class_name} module parsing")
                temp_data = temp_class.get_complex_data()
                log("good", f"Successful {class_name} module parsing")
                return class_name, temp_data

    def handle_parsers(self) -> dict:
        classes_dict: dict = self.get_modules_classes()
        data: dict = dict()
        types: list = list()

        if len(classes_dict.keys()) == 1:
            types = Recognizer(self.input_data).get_data_types_list()
            if len(types) == 1:
                self.input_data: str = Converter(self.input_data, types[0]).get_converted_data()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            partial_process_class = partial(self.process_class, input_data=self.input_data, types=types)

            futures = {executor.submit(partial_process_class, category, class_): class_ for category, class_list in
                       classes_dict.items() for class_ in class_list}

            for future in concurrent.futures.as_completed(futures):
                try:
                    class_name, temp_data = future.result()
                    if class_name is not None:
                        data[class_name] = temp_data
                except TypeError:
                    pass

        return data


def main():
    pass


if __name__ == "__main__":
    main()
