#!/bin/sh
until cd /app/
do
    echo "Waiting for server volume..."
done

until uvicorn main:app --reload --host 0.0.0.0 --port 8000
do
    echo "Starting api..."
    sleep 10
done