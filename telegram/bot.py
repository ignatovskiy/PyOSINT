import json
import os

import requests
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update


def get_token():
    with open("token.json", 'r', encoding="UTF-8") as f:
        bot_token = json.load(f)['TOKEN']
    return bot_token


def dump_results(filename, data):
    with open(filename, 'w', encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


async def run_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    text = message.text
    filename = f"{message.chat_id}-{message.message_id}.json"
    response = requests.post('http://127.0.0.1:8003/search/',
                             json={'search': text,
                                   'category': 'web'})
    if response.status_code == 200:
        search_results = response.json()
        dump_results(filename, search_results)
        print(search_results)
        await message.reply_document(filename,
                                     caption=f"Результаты поиска:\n{text}",
                                     filename="results.json")
        os.remove(filename)
    else:
        await message.reply_text("Unknown error. Please, try again.")


def main():
    pass


if __name__ == "__main__":
    token = get_token()
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, run_search, block=False))
    app.run_polling()
