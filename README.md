# PyOSINT
universal OSINT-tool written in Python language

# Personal Data Anonymizer  
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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
