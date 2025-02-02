from pydantic import BaseModel
from typing import Dict, Optional


class Beer(BaseModel):
    """
    A Pydantic model to represent a beer.
    Contains all the information about a beer.
    """
    name: str
    style: Optional[str] = None
    abv: Optional[str] = None
    epm: Optional[str] = None
    ibu: Optional[str] = None # not used for now
    brewery: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None # not used for now
    rating: Optional[str] = None
    id: Optional[int] = None

    def set(self, key, value):
        setattr(self, key, value)

    def get(self, key):
        return getattr(self, key)


class ScrapeStatusResponse(BaseModel):
    """
    A Pydantic model to represent the response from celery task status check.
    Contains the status of the task and progress if task is still running.
    """
    status: str
    progress: Optional[Dict[str, Optional[int]]]