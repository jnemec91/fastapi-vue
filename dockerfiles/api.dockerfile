FROM python:3.9

WORKDIR /app/

COPY ../requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ../ .

RUN addgroup --system celery && adduser --system --group celery
RUN chmod +x ./worker/celery-entrypoint.sh

RUN pytest

CMD ["fastapi", "run", "./app/main.py", "--proxy-headers", "--port", "8000"]
