# FastAPI + Vue.js Application

A modern web application using FastAPI backend with Vue.js frontend, Celery for background tasks, and PostgreSQL for data storage.

## Features
- Scrape website for beer data and show them in the table
- Scraping is ran as background task
- Table has filters and ordering buttons

## Architecture

The application consists of several containerized services:

- **API**: FastAPI backend server
- **Frontend**: Vue.js web application
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
CELERY_BROKER_URL= redis url
CELERY_RESULT_BACKEND= redis url
POSTGRES_DB= database name
POSTGRES_USER= database user
POSTGRES_PASSWORD= database password
DB_HOST=pgdatabase
DB_PORT=5432
```

Build and start the services:
```
docker-compose up
```

Service Endpoints
```
Frontend: http://localhost:80 (only this should be accessible from outside)
API: http://localhost:8000
PostgreSQL: localhost:5432
```

### Project Structure
```
├── api_worker/         # Celery tasks
├── frontend/          # Vue.js frontend application
├── scraper/           # Web scraping modules
├── celery/            # Celery donfiguration
├── nginx/             # Nginx configuration
├── dockerfiles/       # Docker build files
├── docker-compose.yml
├── api-entrypoint.sh  # entrypoint script for FastAPI app
├── main.py            # FastAPI application
├── .env               # Environment variables
├── readme.md          # This file
└── requirements.txt   # Python app requirements
```
### Contributors
[Jaroslav Němec](https://github.com/jnemec91) - Creator and maintainer

