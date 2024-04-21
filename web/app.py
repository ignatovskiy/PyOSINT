import argparse
import json
import uuid

from flask import Flask, render_template, request, session, url_for, redirect
from flask_babel import Babel, lazy_gettext
import requests
from werkzeug.exceptions import HTTPException

from pyosint.core.constants.categories import CATEGORIES


app = Flask(__name__)


def get_locale():
    return session.get('lang', 'en')


@app.context_processor
def inject_locale():
    return dict(get_locale=get_locale)


def load_translations():
    lang = get_locale()
    with open(f'{TRANSLATIONS_DIR}/{lang}.json', 'r') as file:
        return json.load(file)


app.config['SECRET_KEY'] = str(uuid.uuid4())
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)


@app.route('/switch_lang/<lang>')
def switch_lang(lang):
    if lang in ['en', 'ru']:
        session['lang'] = lang
    referrer = request.referrer
    return redirect(referrer)


@app.route('/', methods=['GET', 'POST'])
def home():
    texts = load_translations()
    search_results = []
    options_list = CATEGORIES.keys()
    if request.method == 'POST':
        search_query = request.form.get('query', '')
        selected_option = request.form.get('option', None)
        try:
            response = requests.post(f"http://{API_IP}:{API_PORT}/search/",
                                     json={'search': search_query,
                                           'category': selected_option})
            if response.status_code == 200:
                search_results = response.json()
        except requests.exceptions.ConnectionError:
            return render_template('errors/connection.html', texts=texts), 500
    return render_template('index.html', search_results=search_results, options_list=options_list,
                           texts=texts)


@app.route('/agreement')
def agreement():
    texts = load_translations()
    return render_template('agreement.html', texts=texts)


@app.errorhandler(HTTPException)
def handle_exception(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = e.get_response()

        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    texts = load_translations()
    return render_template('errors/error_generic.html', error=e, texts=texts), e.code


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="-p PORT -i IP -ap API_PORT")

    parser.add_argument('-i', '--ip', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-p', '--port', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-ap', '--api_port', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-ai', '--api_ip', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-tr', '--translations_dir', type=str, help=argparse.SUPPRESS)

    args = parser.parse_args()

    IP = "127.0.0.1"
    PORT = 8080
    API_IP = "127.0.0.1"
    API_PORT = "9000"
    TRANSLATIONS_DIR = "translations"

    PORT = int(args.port) if args and args.port else PORT
    IP = args.ip if args and args.ip else IP
    API_IP = args.api_ip if args and args.api_ip else API_IP
    API_PORT = args.api_port if args.api_port else API_PORT
    TRANSLATIONS_DIR = args.translations_dir if args.translations_dir else TRANSLATIONS_DIR

    app.run(host=IP, port=PORT)
