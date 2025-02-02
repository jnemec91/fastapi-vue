import os
import time
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from core.models import ScrapeStatusResponse
from core.database import Database, connect_and_create
from core.models import Beer
from worker.tasks import scrape_web_for_the_beers

logging.basicConfig(level=logging.INFO)

running_tasks = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.info("Starting BeerAPI")

# Create and connect to the database on startup
db = connect_and_create(create=True)

@app.get("/beers")
async def get_all_beers() -> list[Beer]:
    """
    Get all beers from the database.

    Returns:
    list: List of all beers (Beer objects from scraper.beer)
    """
    data = db.fetch()
    return data

@app.get("/beers/scrape")
async def scrape_beers() -> dict[str, str]:
    """
    Scrape the web for beers.
    If a scraping task is already running, return the task ID.

    Returns:
    dict: Task ID of the scraping task
    """
    if running_tasks:
        logging.info("Scraping already in progress")
        return {"task_id": running_tasks[0]}
    
    logging.info("Scraping beers")
    task = scrape_web_for_the_beers.delay()
    running_tasks.append(task.id)
    return {"task_id": task.id}

@app.get("/tasks/running")
async def get_tasks() -> dict[str, list[str]]:
    """
    Get all running celery tasks.
    Based on how app is written this should always be list with only one or zero tasks.

    """
    return {"tasks": running_tasks}

@app.get("/beers/tasks/{task_id}")
async def get_scrape_status(task_id: str) -> ScrapeStatusResponse:
    """
    Get the status of a celery task based on id provided.

    Args:
    task_id (str): Celery task id

    Returns:
    dict: Status of the task and progress if task is still running
    """
    task = AsyncResult(task_id)
    if task.ready():
        running_tasks.remove(task_id)
        return {
            "status": task.status,
            "progress": task.info, # task.info should be None if task is not running

            # Not going to implement task results in frontend for now
            # "result": task.get() if task.successful() else str(task.result)
        }
    elif task.state == 'PROGRESS':
        return {
            "status": task.state,
            # task info is a dict with keys 'current'and 'total' containing progress info (int)
            "progress": task.info
        }        
    return {
        "status": task.status,
        "progress": task.info
        }
