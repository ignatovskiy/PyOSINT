from recognizer import Recognizer
from converter import Converter


def main():
    a = Recognizer("1.1.1.1").get_data_types_list()
    b = Converter('+7(800)000-00-00', 'phone').get_converted_data()
    print(b)


if __name__ == "__main__":
    main()
