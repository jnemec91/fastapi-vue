import os
import re
import bs4
import time
import requests
import unicodedata
import logging
from celery import Celery
from core.models import Beer
from core.utils import construct_url
from core.database import Database, connect_and_create

logging.basicConfig(level=logging.INFO)

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
celery.conf.broker_connection_retry_on_startup = True


@celery.task(name="scrape_web_for_the_beers")
def scrape_web_for_the_beers() -> None:
    """
    This task scrapes the website for beers and stores them in the database.

    Returns:
    None
    """
    logging.info("Scraping beers")

    database = connect_and_create()

    response = requests.get(construct_url("http", "www.atlaspiv.cz/", "?page=hodnoceni"))
    response.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    all_rows = soup.find_all('tr')


    for progress,beer in enumerate(all_rows):
        scrape_web_for_the_beers.update_state(
            state='PROGRESS',
            meta={'current': progress, 'total': len(all_rows)}
        )

        logging.info(f"Scrape progress: {progress}/{len(all_rows)}")

        beer_name_tag = beer.find('a', class_='beername hinted')
        if not beer_name_tag:
            continue

        beer_name = beer_name_tag.text.strip()
        beer_url = construct_url("http", "www.atlaspiv.cz/", beer_name_tag['href'])
        beer_style = beer.find_all('td')[-1].text.strip()
        beer_rating = beer.find_all('span', class_='invisible')[-1].text.strip() + "/10"

        # follow to the detail page to get more information
        response = requests.get(beer_url)
        response.encoding = 'utf-8'
        beer_soup = bs4.BeautifulSoup(response.text, 'html.parser')

        try:
            beer_abv = re.search(
                r'\d+\.\d+\s?%',beer_soup.find_all('tr')[4].text.strip()).group().replace('%', '')
        except AttributeError:
            beer_abv = "N/A"

        # get beer epm
        try:
            beer_epm = re.search(
                r'\d+\.\d+\s?°',beer_soup.find_all('tr')[6].text.strip()).group().replace('°', '')
        except AttributeError:
            beer_epm = "N/A"

        # get beer brewery
        try:
            beer_brewery = beer_soup.find(
                'span', {"id": "brewery_name_result"}).find('a').text.strip()
            beer_brewery = unicodedata.normalize('NFKC', beer_brewery)
        except AttributeError:
            beer_brewery = "N/A"

        # get beer location
        try:
            beer_location = beer_soup.find(
                'span', {"id": "brewery_name_result"}).text.replace(beer_brewery, "")[1::].strip()
            beer_location = unicodedata.normalize('NFKC', beer_location)
        except AttributeError:
            beer_location = "N/A"

        # get beer description
        try:
            beer_description = beer_soup.find('i').text.strip()
            beer_description = unicodedata.normalize('NFKC', beer_description)
        except AttributeError:
            beer_description = "N/A"

        beer = Beer(name=beer_name)
        beer.set('style', beer_style)
        beer.set('abv', beer_abv)
        beer.set('epm', beer_epm)
        beer.set('ibu', None) # not used for now
        beer.set('brewery', beer_brewery)
        beer.set('location', beer_location)
        beer.set('description', beer_description)
        beer.set('url', beer_url)
        beer.set('image_url', None) # not used for now
        beer.set('rating', beer_rating)

        db_beer = database.find_fuzzy(beer)
        if not db_beer:
            database.insert(beer)
        
        else:
            logging.info(f"Updating beer: {beer.name}")
            database.update(int(db_beer[0].id), beer)