SYMBOLS_TO_REMOVE = ['\n', '\t', '\xa0', '\"']
TRANSLATION_TABLE = str.maketrans("", "", "".join(SYMBOLS_TO_REMOVE))
