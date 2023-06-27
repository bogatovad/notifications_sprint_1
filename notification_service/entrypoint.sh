#!usr/bin/env bash

echo "RabbitMQ not yet run..."
# Проверяем доступность хоста и порта
while ! nc -z $RABBIT_HOST $RABBIT_PORT; do
  sleep 0.1
done
echo "RabbitMQ did run."

gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker