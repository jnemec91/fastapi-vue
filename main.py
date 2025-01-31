import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper.database import Database
from celery.result import AsyncResult
import logging
from api_worker.tasks import scrape_web_for_the_beers

running_tasks = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://http://127.0.0.1:80", "http://localhost:80"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database(os.getenv('POSTGRES_DB'), os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_PORT'))
db.create()
db.connect()

logging.basicConfig(level=logging.INFO)
logging.info("Starting BeerAPI")

@app.get("/beers")
async def get_all_beers():
    db.connect()
    data = db.fetch()
    return data

@app.get("/beers/scrape")
async def scrape_beers():
    if running_tasks:
        logging.info("Scraping already in progress")
        return {"task_id": running_tasks[0]}
    
    logging.info("Scraping beers")
    task = scrape_web_for_the_beers.delay("scrape")
    running_tasks.append(task.id)
    return {"task_id": task.id}

@app.get("/tasks/running")
async def get_tasks():
    return {"tasks": running_tasks}

@app.get("/beers/tasks/{task_id}")
async def get_scrape_status(task_id: str):
    task = AsyncResult(task_id)
    if task.ready():
        running_tasks.remove(task_id)
        return {
            "status": task.status,
            "result": task.get() if task.successful() else str(task.result)
        }
    return {"status": task.status}
