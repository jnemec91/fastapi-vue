from .scraper import get_beer_list_atlas
from .database import Database

if __name__ == "__main__":    
    get_beer_list_atlas("http","www.atlaspiv.cz/","?page=hodnoceni", "../beers.db")


