# PyOSINT
universal OSINT-tool written in Python language


[![Build Status](https://github.com/ignatovskiy/PyOSINT/actions/workflows/python-app.yml/badge.svg)](https://github.com/ignatovskiy/PyOSINT/actions)
![](https://img.shields.io/github/license/ignatovskiy/PyOSINT)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyOsint.

```bash
pip install .
```


## Usage

Parsing data to JSON
```bash
python3 pyosint python3 pyosint -d [INPUT DATA] -o json -f [OUTPUT FILE]
```

Parsing data to PDF
```bash
python3 pyosint python3 pyosint -d [INPUT DATA] -o pdf -f [OUTPUT FILE]
```

Parsing data with defined category
```bash
python3 pyosint python3 pyosint -d [INPUT DATA] -o pdf -f [OUTPUT FILE] -c [CATEGORY]
```


## Adding modules

You can easily add your own module by there steps:

1. Create .py file with name of your module
2. Move this file to pyosint/modules/%CATEGORY%/ where %CATEGORY% is category of parsed data from your module (company/web/person)
3. Add mandatory structure:
```python
from pyosint.core.utils import *


URL = "URL_FROM_OSINT_WEBSITE_FOR_YOUR_MODULE"


class YourModuleName:
    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url): #  must return bs4 soup object or dict with data
        return

    def get_search_url(input_data): #  must return URL for requests with input_data
        return

    def get_complex_data(self): #  must return final dict with data
        return
```
4. That's it!


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
