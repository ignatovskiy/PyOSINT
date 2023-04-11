from recognizer import Recognizer


def main():
    a = Recognizer("1.2.3.4.5").get_data_type()
    print(a)


if __name__ == "__main__":
    main()
