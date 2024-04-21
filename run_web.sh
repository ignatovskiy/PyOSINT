#!/bin/bash

HOST="127.0.0.1"
PORT="8080"
FASTAPI_IP="127.0.0.1"
FASTAPI_PORT="9000"
TRANSLATIONS="web/translations"

PID_DIR="./web-pids"
mkdir -p $PID_DIR
FLASK_PID_FILE="$PID_DIR/flask.pid"
FASTAPI_PID_FILE="$PID_DIR/fastapi.pid"

echo "Starting Web Application on http://$HOST:$PORT"
nohup python3 web/app.py --ip $HOST --port $PORT --api_ip $FASTAPI_IP --api_port $FASTAPI_PORT --translations_dir $TRANSLATIONS > /dev/null 2>&1 &
echo $! > $FLASK_PID_FILE

echo "Starting FastAPI on http://$FASTAPI_IP:$FASTAPI_PORT"
nohup uvicorn web.api:app --host $FASTAPI_IP --port $FASTAPI_PORT > /dev/null 2>&1 &
echo $! > $FASTAPI_PID_FILE

echo "Applications are running..."

trap "echo 'Stopping applications...'; kill $(cat $FLASK_PID_FILE); kill $(cat $FASTAPI_PID_FILE); rm -rf $PID_DIR; exit 0" SIGINT SIGTERM

wait