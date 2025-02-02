FROM python:3.9

WORKDIR /app/

COPY ../requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ../ .

RUN addgroup --system celery && adduser --system --group celery
RUN chmod +x ./worker/celery-entrypoint.sh

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
