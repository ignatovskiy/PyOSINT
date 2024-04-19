#!/bin/bash

FASTAPI_IP="127.0.0.1"
FASTAPI_PORT="9200"
TELEGRAM_TOKEN="telegram/token.json"

echo "Starting Telegram Bot"
nohup python3 telegram/bot.py --api_ip $FASTAPI_IP --api_port $FASTAPI_PORT --token_path $TELEGRAM_TOKEN > /dev/null 2>&1 &

echo "Starting FastAPI on $FASTAPI_IP IP and $FASTAPI_PORT PORT"
nohup uvicorn web.api:app --host $FASTAPI_IP --port $FASTAPI_PORT --reload > /dev/null 2>&1 &

echo "Applications are running..."

wait