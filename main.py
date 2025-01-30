from fastapi import FastAPI
from scraper.database import Database

import logging

from api_worker.tasks import scrape_web_for_the_beers


app = FastAPI()
db = Database("beers.db")

logging.basicConfig(level=logging.INFO)
logging.info("Starting BeerAPI")

@app.get("/beers")
def get_all_beers():
    db.connect()
    data = db.fetch()

    return {"data": data}

@app.get("/beers/scrape")
async def scrape_beers():
    logging.info("Scraping beers")
    scrape_web_for_the_beers.delay("scrape", db.name)
