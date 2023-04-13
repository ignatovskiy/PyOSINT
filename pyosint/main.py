from recognizer import Recognizer
from validator import Validator


def main():
    a = Recognizer("1.2.3.4").get_data_type()
    print(a)
    b = Validator(input_data='1.2.3.4', types_dict=a).validate_types()
    print(b)


if __name__ == "__main__":
    main()
