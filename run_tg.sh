#!/bin/bash

FASTAPI_IP="127.0.0.1"
FASTAPI_PORT="9200"
TELEGRAM_TOKEN="telegram/token.json"

PID_DIR="./tg-pids"
mkdir -p $PID_DIR
TG_PID_FILE="$PID_DIR/tg.pid"
FASTAPI_PID_FILE="$PID_DIR/fastapi.pid"

echo "Starting Telegram Bot"
nohup python3 telegram/bot.py --api_ip $FASTAPI_IP --api_port $FASTAPI_PORT --token_path $TELEGRAM_TOKEN > /dev/null 2>&1 &
echo $! > $TG_PID_FILE

echo "Starting FastAPI on $FASTAPI_IP IP and $FASTAPI_PORT PORT"
nohup uvicorn web.api:app --host $FASTAPI_IP --port $FASTAPI_PORT > /dev/null 2>&1 &
echo $! > $FASTAPI_PID_FILE

echo "Applications are running..."

trap "echo 'Stopping applications...'; kill $(cat $FLASK_PID_FILE); kill $(cat $FASTAPI_PID_FILE); rm -rf $PID_DIR; exit 0" SIGINT SIGTERM

wait