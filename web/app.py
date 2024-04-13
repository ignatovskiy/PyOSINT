from flask import Flask, render_template, request, redirect, url_for
import requests

from pyosint.core.constants.categories import CATEGORIES

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    search_results = []
    options_list = CATEGORIES.keys()
    if request.method == 'POST':
        search_query = request.form.get('query', '')
        selected_option = request.form.get('option', None)
        response = requests.post('http://127.0.0.1:8003/search/',
                                 json={'search': search_query,
                                       'category': selected_option})
        if response.status_code == 200:
            search_results = response.json()
    return render_template('index.html', search_results=search_results, options_list=options_list)


@app.route('/agreement')
def agreement():
    return render_template('agreement.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
