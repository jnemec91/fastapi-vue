#!/bin/bash
until cd /app/
do
    echo "Waiting for server volume..."
done

celery -A api_worker.tasks worker --loglevel=info --concurrency=1 -n worker1@%h -E --uid=celery --gid=celery