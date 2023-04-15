from pyosint.core.converter import Converter


def test_convert_phone():
    assert Converter('+7(800)000-00-00', 'phone').get_converted_data() == '78000000000'


def test_convert_hostname():
    assert Converter('https://test.com', 'hostname').get_converted_data() == 'test.com'


def test_convert_id():
    assert Converter('10-20 30 40-50', 'id').get_converted_data() == '1020304050'
