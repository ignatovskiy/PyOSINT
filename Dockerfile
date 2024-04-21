FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

EXPOSE 8080 9000
