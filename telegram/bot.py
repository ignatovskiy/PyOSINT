import argparse
import json
import os

import requests
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update


def get_token():
    with open(TOKEN_PATH, 'r', encoding="UTF-8") as f:
        bot_token = json.load(f)['TOKEN']
    return bot_token


def dump_results(filename, data):
    with open(filename, 'w', encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


async def run_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    text = message.text
    filename = f"{message.chat_id}-{message.message_id}.json"
    response = requests.post(f"http://{API_IP}:{API_PORT}/search/",
                             json={'search': text,
                                   'category': 'web'})
    if response.status_code == 200:
        search_results = response.json()
        dump_results(filename, search_results)
        await message.reply_document(filename,
                                     caption=f"Результаты поиска:\n{text}",
                                     filename="results.json")
        os.remove(filename)
    else:
        await message.reply_text("Unknown error. Please, try again.")


def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="-ai API_IP -ap API_PORT")

    parser.add_argument('-t', '--token_path', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-ai', '--api_ip', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-ap', '--api_port', type=str, help=argparse.SUPPRESS)
    args = parser.parse_args()

    API_IP = "127.0.0.1"
    API_PORT = "9000"
    TOKEN_PATH = "token.json"

    API_IP = args.api_ip if args and args.api_ip else API_IP
    API_PORT = args.api_port if args.api_port else API_PORT
    TOKEN_PATH = args.token_path if args.token_path else TOKEN_PATH

    token = get_token()
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, run_search, block=False))
    app.run_polling()
