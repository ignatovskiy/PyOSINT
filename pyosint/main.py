from recognizer import Recognizer
from converter import Converter
from parser import Parser


def main():
    a = Parser("https://google.com", "get").get_all_attrs_values("a", "href")
    print(a)


if __name__ == "__main__":
    main()
