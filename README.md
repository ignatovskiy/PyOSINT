# PyOSINT
universal OSINT-tool written in Python language


[![Build Status](https://github.com/ignatovskiy/PyOSINT/actions/workflows/python-app.yml/badge.svg)](https://github.com/ignatovskiy/PyOSINT/actions)
![](https://img.shields.io/github/license/ignatovskiy/PyOSINT)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# Usage

## Console

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyOsint.

```bash
pip install -e .
```

### Running

Parsing data to JSON:
```bash
python3 pyosint -d <input_data> -o json -f <output_file>
```

Parsing data to PDF:
```bash
python3 pyosint -d <input_data> -o pdf -f <output_file>
```

Parsing data with defined category:
```bash
python3 pyosint -d <input_data> -o <output_type> -f <output_file> -c <category>
```

Example (try it):
```bash
python3 pyosint -d 1.1.1.1 -o json -f cloudflare.json
```

## Docker

Fill .env file with correct values (but it can work with default ones)

### Run FastAPI interface only

```bash
docker compose up fastapi_app -d
```

**HTTP Method:** `POST`
**Endpoint:** `/search/`

**Description:** Sends a search query along with a selected category to the search endpoint.

**Request Body:**

- `search` (string, required): The search query.
- `category` (string, required): The category to search within (web, person, company, file).

**Example:**

POST http://0.0.0.0:9000/search/
Content-Type: application/json

{
  "search": "1.1.1.1",
  "category": "web"
}


### Run Web interface

```bash
docker compose up flask_app -d
```

Open http://<HOST_IP>:<WEB_PORT> in browser

**Example:**

http://0.0.0.0:8080


### Run Telegram bot interface

Paste your Telegram Bot token to telegram/token.json (value of "TOKEN" key)

```bash
docker compose up tg_app -d
```

Open your Telegram Bot and write input data

**Example:**

pyosint_demo_bot

## SH scripts (Linux&macOS)

### Run Web interface

Paste your values to run_web.sh script

```bash
./run_web.sh
```

### Run Telegram bot interface

Paste your values to run_tg.sh script

```bash
./run_tg.sh
```

# Adding modules

You can easily add your own module by there steps:

1. Create .py file with name of your module
2. Move this file to pyosint/modules/<CATEGORY>/ where <CATEGORY> is category of parsed data from your module (company/web/person/file)
3. Copy mandatory structure which corresponding to your module category from templates/%category%.py

**Example for web category:**
```python
from pyosint.core.categories.web import Web
from pyosint.core.cmd import handle_cmd_args_module


URL = ""


class WebModule(Web):
    types = []

    def __init__(self, input_data, data_type=None):
        self.input_data = input_data
        self.data_type = [data_type]

    def get_parsed_object(self, url):
        return self.get_soup_from_raw(self.get_request_content(self.make_request('get', url)))

    def get_search_url(self, input_data):
        return f"{URL}/{input_data}"

    def get_complex_data(self):
        parsed = self.get_parsed_object(self.get_search_url(self.input_data))
        return parsed


def main():
    handle_cmd_args_module(WebModule)


if __name__ == "__main__":
    main()
```
4. Add URL of service to URL constant, unique module name to class name and as handle_cmd_args_module argument, parsing/handling logic to functions
5. That's it!

# Run module directly for testing

You can run each module directly

```bash
cd <SCRIPT_FOLDER>
python script.py <input_data> [--data_type <data_type>] [--hidden] [--json [<json_file>]] [--dir <output_dir>]
```

Arguments:

input_data (str): Input data for parsing.
--data_type (str, optional): Specifies the input data type. Default is None.
--hidden (flag, optional): Hides the result print if set.
--json (str, optional): Saves the result to a JSON file. If no file name is provided, a default name will be used.
--dir (str, optional): Specifies the output directory for saving files. Default is the current directory (.).

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


# License
[MIT](https://choosealicense.com/licenses/mit/)
