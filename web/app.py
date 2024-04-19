import argparse

from flask import Flask, render_template, request
import requests

from pyosint.core.constants.categories import CATEGORIES


app = Flask(__name__)


def run_flask():
    app.run(host=IP, port=PORT)


@app.route('/', methods=['GET', 'POST'])
def home():
    search_results = []
    options_list = CATEGORIES.keys()
    if request.method == 'POST':
        search_query = request.form.get('query', '')
        selected_option = request.form.get('option', None)
        response = requests.post(f"http://{API_IP}:{API_PORT}/search/",
                                 json={'search': search_query,
                                       'category': selected_option})
        if response.status_code == 200:
            search_results = response.json()
    return render_template('index.html', search_results=search_results, options_list=options_list)


@app.route('/agreement')
def agreement():
    return render_template('agreement.html')


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="-p PORT -i IP -ap API_PORT")

    parser.add_argument('-i', '--ip', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-p', '--port', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-ap', '--api_port', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-ai', '--api_ip', type=str, help=argparse.SUPPRESS)

    args = parser.parse_args()

    IP = "127.0.0.1"
    PORT = 8080
    API_IP = "127.0.0.1"
    API_PORT = "9200"

    PORT = int(args.port) if args and args.port else PORT
    IP = args.ip if args and args.ip else IP
    API_IP = args.api_ip if args and args.api_ip else API_IP
    API_PORT = args.api_port if args.api_port else API_PORT

    app.run(host=IP, port=PORT)
