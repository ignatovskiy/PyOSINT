from pyosint.recognizer import Recognizer


def test_phone_ru_brackets():
    assert Recognizer("+7(900)100-20-30").is_phone() is True


def test_phone_ru_numbers():
    assert Recognizer("88005006030").is_phone() is True


def test_phone_ru_plus():
    assert Recognizer("+79994005060").is_phone() is True


def test_phone_us_dots():
    assert Recognizer("432.443.491").is_phone() is True


def test_phone_us_numbers():
    assert Recognizer("50100").is_phone() is True


def test_phone_invalid_letter():
    assert Recognizer("8800A").is_phone() is False


def test_phone_invalid_character():
    assert Recognizer("-800").is_phone() is False


def test_phone_plus_end():
    assert Recognizer("8800+").is_phone() is False
