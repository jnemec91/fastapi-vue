import bs4
import requests
import re
from .beer import Beer
from .database import Database

def construct_url(protocol: str, server: str, url: str) -> str:
    return protocol+"://"+server+url

def get_beer_list_atlas(protocol: str, server: str, url: str, db: str) -> list:

    # create database connection
    database = Database(db)
    database.create(db)
    database.connect()

    print(f"Database connection established to: {database}")    
    print(f"Fetching beers from: {construct_url(protocol, server, url)}")

    response = requests.get(construct_url(protocol, server, url))
    response.encoding = response.apparent_encoding
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    all_rows = soup.find_all('tr')
    progress = 0
    complete = len(all_rows)

    for beer in all_rows:
        # show progress
        print(f"Progress: {'█'*(progress//(complete // 10))}{' '*(10-progress//(complete // 10))} {progress}/{complete}", end="\r")
        progress += 1

        beer_name_tag = beer.find('a', class_='beername hinted')
        if not beer_name_tag:
            continue

        beer_name = beer_name_tag.text.strip()
        beer_url = construct_url(protocol, server, beer_name_tag['href'])
        beer_style = beer.find_all('td')[-1].text.strip()
        beer_rating = beer.find_all('span', class_='invisible')[-1].text.strip() + "/10"

        # follow to the detail page to get more information
        response = requests.get(beer_url)
        response.encoding = response.apparent_encoding
        beer_soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # get beer percentage
        try:
            beer_abv = re.search(r'\d+\.\d+\s?%',beer_soup.find_all('tr')[4].text.strip()).group().replace('%', '')
        except AttributeError:
            beer_abv = "N/A"

        # get beer epm
        try:
            beer_epm = re.search(r'\d+\.\d+\s?°',beer_soup.find_all('tr')[6].text.strip()).group().replace('°', '')
        except AttributeError:
            beer_epm = "N/A"

        # get beer brewery
        try:
            beer_brewery = beer_soup.find('span', {"id": "brewery_name_result"}).find('a').text.strip()
        except AttributeError:
            beer_brewery = "N/A"

        # get beer location
        try:
            beer_location = beer_soup.find('span', {"id": "brewery_name_result"}).text.replace(beer_brewery, "")[1::].strip()
        except AttributeError:
            beer_location = "N/A"

        # get beer description
        try:
            beer_description = beer_soup.find('i').text.strip()
        except AttributeError:
            beer_description = "N/A"

        beer = Beer(beer_name)
        beer.set('style', beer_style)
        beer.set('abv', beer_abv)
        beer.set('epm', beer_epm)
        beer.set('brewery', beer_brewery)
        beer.set('location', beer_location)
        beer.set('description', beer_description)
        beer.set('url', beer_url)
        beer.set('image_url', None)
        beer.set('rating', beer_rating)

        # insert into database
        db_beer = database.find_fuzzy(beer)

        if not db_beer:
            # print(f"Inserting beer: {beer.name}")
            database.insert(beer)
        
        else:
            print(f"Beer already in database: {beer.name}")
            # update beer
            print(f"Updating beer: {beer.name}")
            database.update(db_beer[0].id, beer)

    return database.fetch()