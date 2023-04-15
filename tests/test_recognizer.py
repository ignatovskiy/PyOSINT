from pyosint.recognizer import Recognizer


# Phone tests
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


# IP tests
def test_ip_v4():
    assert Recognizer("1.2.3.4").is_ip() is True


def test_ip_v4_invalid_letter():
    assert Recognizer("1.2.3.A").is_ip() is False


def test_ip_v4_invalid_range():
    assert Recognizer("1.2.3.4.5").is_ip() is False


def test_ip_v6_skips():
    assert Recognizer("2001:db8:85a3:8d3:1319:8a2e:370:7348").is_ip() is True


def test_ip_v6_full():
    assert Recognizer("2001:0db8:0000:0000:0000:ff00:0042:8329").is_ip() is True


def test_ip_v6_short():
    assert Recognizer("fe80::1").is_ip() is True


def test_ip_v6_complex():
    assert Recognizer("fe80::200:5aee:feaa:20a2").is_ip() is True


def test_ip_v6_invalid_letter():
    assert Recognizer("2001:db8:85a3:8d3:1319:8a2e:370:734g").is_ip() is False


def test_ip_v6_invalid_extra_colon():
    assert Recognizer("fe80:::1").is_ip() is False


def test_ip_v6_invalid_trailing_colon():
    assert Recognizer("2001:0db8:0000:0000:0000:ff00:0042:8329:").is_ip() is False


def test_ip_v6_invalid_long_hextet():
    assert Recognizer("2001:0db8:85a3:0000:0000:8a2e:370:73345").is_ip() is False


def test_email():
    assert Recognizer("john@example.com").is_email() is True


def test_email_multi_domains():
    assert Recognizer("david@example.co.uk").is_email() is True


def test_email_invalid_domain_name():
    assert Recognizer("john@.com").is_email() is False


def test_email_invalid_missing_tld():
    assert Recognizer("joe@hotmail").is_email() is False


def test_email_invalid_extra_char():
    assert Recognizer("sarah@my!email.com").is_email() is False


def test_email_invalid_extra_dot():
    assert Recognizer("andrew@gmail..com").is_email() is False


def test_email_invalid_short_tld():
    assert Recognizer("lisa@yahoo.c").is_email() is False


def test_hostname_line():
    assert Recognizer("my-server.com").is_hostname() is True


def test_hostname_www():
    assert Recognizer("www.example.com").is_hostname() is True


def test_hostname_multi_domains():
    assert Recognizer("dev.my-server.co.uk").is_hostname() is True


def test_hostname_invalid_extra_dot():
    assert Recognizer("myserver.co..uk").is_hostname() is False


def test_hostname_invalid_symbol():
    assert Recognizer("_my_server.com").is_hostname() is False


def test_name():
    assert Recognizer("Katie Brown").is_name() is True


def test_name_invalid_symbol():
    assert Recognizer("@lex").is_name() is False


def test_name_invalid_numbers():
    assert Recognizer("Lily22").is_name() is False


def test_address():
    assert Recognizer("789 Oak Ave, Los Angeles, CA 90001").is_address() is True


def test_address_invalid_symbol():
    assert Recognizer("444 Elm St, Apt 3C#").is_address() is False


def test_company_ru_quotes():
    assert Recognizer('ООО "Мир"').is_company_name() is True


def test_company_ru_symbol():
    assert Recognizer("Красное & Белое").is_company_name() is True


def test_company_en_quotes():
    assert Recognizer('LLC "Mir"').is_company_name() is True


def test_company_en_inc():
    assert Recognizer("Russian Inc.").is_company_name() is True


def test_company_en_symbol():
    assert Recognizer("Elon Musk's Companies").is_company_name() is True


def test_nick():
    assert Recognizer("t3$t").is_nickname() is True
