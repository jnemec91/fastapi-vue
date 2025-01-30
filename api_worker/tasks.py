import os
import time

from celery import Celery
from scraper.scraper import get_beer_list_atlas
from scraper.database import Database

db = Database("beers.db")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery.conf.broker_connection_retry_on_startup = True


@celery.task(name="scrape_web_for_the_beers")
def scrape_web_for_the_beers(task_type, db_name):
    db.connect()
    get_beer_list_atlas("http", "www.atlaspiv.cz/", "?page=hodnoceni", db_name)
    
    return {"message": "done"}
