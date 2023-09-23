# regexp statements
EMAIL_REGEXP = r"^[A-Za-z0-9\._%\+\-]+@([A-Za-z0-9\-]+\.)+[A-Z|a-z]{2,}$"
PHONE_REGEXP = r"^[\+\(]?[1-9][0-9 .\-\(\)]{0,}[0-9\(\)]$"
IP_REGEXP = r"^((\b(\d{1,3}\.){3}(\d{1,3})\b)|([A-Fa-f0-9]{1,4}:{1,2}){1,7}([A-Fa-f0-9]{1,4}))$"
HOST_REGEXP = r"^(https?:\/\/)?(([A-Za-zА-Яа-я0-9\-])+\.)+([A-Za-zА-Яа-я0-9]+)$"
NAME_REGEXP = r"^([A-Za-zА-Яа-я]+ )+([A-Za-zА-Яа-я]+)$"
NICK_REGEXP = r"^[\w!@\$%#&\-\?<>~]+$"
ADDRESS_REGEXP = r"^[а-яА-ЯёЁa-zA-Z0-9\s\.\,\-\/№\(\)&\'\"]+$"
COMPANY_REGEXP = r"^[а-яА-ЯёЁa-zA-Z\s\d&\(\)\[\]\.\,\-\'\"/]+$"
ID_REGEXP = r"^[0-9 \-]+$"


# personal data categories
CATEGORIES = {
    "person": {"email", "phone", "address", "nickname", "id", "name"},
    "web": {"ip", "hostname"},
    "company": {"address", "company", "id"}
}

# user-agent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"


# exclusions
EXCLUDE_TYPES = ["ip", "email"]
EXCLUDE_MODULES = ["test.py", "__init__.py"]
EXCLUDE_NAMES = ["Recognizer", "soup"]
