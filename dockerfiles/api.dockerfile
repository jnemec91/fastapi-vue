FROM python:3.9

WORKDIR /app/

COPY ../requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ../ .

# create user and group for celery
RUN addgroup --system celery && adduser --system --group celery

# assign permission to the entrypoint script
RUN chmod +x ./celery/celery-entrypoint.sh

# CMD ["fastapi", "run", "app/main.py", "--port", "8000"]