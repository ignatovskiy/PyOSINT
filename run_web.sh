#!/bin/bash

HOST="127.0.0.1"
PORT="8080"
FASTAPI_IP="127.0.0.1"
FASTAPI_PORT="9200"

echo "Starting Web Application on $HOST IP and $PORT PORT"
nohup python3 web/app.py --ip $HOST --port $PORT --api_ip $FASTAPI_IP --api_port $FASTAPI_PORT > /dev/null 2>&1 &

echo "Starting FastAPI on $FASTAPI_IP IP and $FASTAPI_PORT PORT"
nohup uvicorn web.api:app --host $FASTAPI_IP --port $FASTAPI_PORT --reload > /dev/null 2>&1 &

echo "Applications are running..."

wait