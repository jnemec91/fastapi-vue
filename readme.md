# FastAPI + Vue.js Application

A modern web application using FastAPI backend with Vue.js frontend, Celery for background tasks, and PostgreSQL for data storage.

## Features
- Scrape website for beer data and show them in the table
- Scraping is ran as background task
- Table has filters, ordering buttons, pagination and modals with detail info about beer

## Architecture

The application consists of several containerized services:

- **API**: FastAPI backend server
- **Frontend**: Vue.js web application and NGINX web server
- **Worker**: Celery worker for background task processing
- **Redis**: Message broker for Celery
- **PostgreSQL**: Main database

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository

2. Create a `.env` file in the root directory with the following variables:
```
VUE_APP_API_BASE_URL= fastapi_url       # Must be set - sets urls in frontend to point to fastapi
CELERY_BROKER_URL= redis_url            # Defaults to "redis://redis:6379" when not set
CELERY_RESULT_BACKEND= redis_url        # Defaults to ""redis://redis:6379" when not set
POSTGRES_DB= database_name              # Defaults to value of POSTGRES_USER when not set (see postgres docker image)
POSTGRES_USER= database_user            # Defaults to "postgres" when not set (see postgres docker image)
POSTGRES_PASSWORD= database_password    # Must be set
DB_HOST= pgdatabase                     # Must be set to name of database service ("pgdatabase" with listed yml file)
DB_PORT= 5432                           # Must be set to port used by database service (5432 with listed yml file)
DB_TIMEOUT_MAX_BACKOFF=60               # Defaults to 64 when not set
```

Build and start the services:
```
docker-compose up
```

Service Endpoints
```
Frontend: http://frontend:80 (only this will be accessible from outside)
          http://frontend:8000

API: http://api:8000         (this will be accessible as well)
PostgreSQL: pgdatabase:5432
```

### Project Structure
```
├── app/               # FastAPI application
│   ├── __init__.py
│   └── main.py
├── core/              # Core modules
│   ├── __init__.py
│   ├── database.py    # Database class
│   ├── models.py      # Pydantic models
│   └── utils.py       # Utility functions
├── dockerfiles/       # Docker build files
│   ├── api.dockerfile
│   └── frontend.dockerfile
├── frontend/          # Vue.js frontend application
│   ├── src/           # Vue js views, components and router
│   └── ...
├── nginx/             # Nginx configuration
│   └── nginx.conf
├── worker/            # Celery tasks and configuration
│   └── celery-entrypoint.sh
├── .dockerignore
├── .env               # Environment variables
├── .gitignore
├── docker-compose.yml
├── readme.md          # This file
├── requirements.txt   # Python app requirements
└── todo
```
### Contributors
[Jaroslav Němec](https://github.com/jnemec91) - Creator and maintainer

