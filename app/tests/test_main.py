from fastapi import FastAPI
from fastapi.testclient import TestClient
from ..main import app
from unittest.mock import patch, MagicMock
from core.models import Beer


class TestDatabase:
    def fetch(self):
        return []

client = TestClient(app)

def test_get_all_beers():
    """Test getting all beers with mocked database data"""
    test_beers = [
        Beer(name="Test Beer 1",
             style="Test Style 1",
             abv="Test ABV 1",
             epm="Test EPM 1",
             brewery="Test Brewery 1",
             location="Test Location 1",
             description="Test Description 1",
             url="Test URL 1",
             image_url="Test Image URL 1",
             rating="Test Rating 1",
             id=1),
        Beer(name="Test Beer 2",
            style="Test Style 2",
            abv="Test ABV 2",
            epm="Test EPM 2",
            brewery="Test Brewery 2",
            location="Test Location 2",
            description="Test Description 2",
            url="Test URL 2",
            image_url="Test Image URL 2",
            rating="Test Rating 2",
            id=2)
    ]
    
    with patch('core.database.Database.fetch') as mock_fetch:
        mock_fetch.return_value = test_beers
        response = client.get("/beers")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "Test Beer 1"

def test_get_all_beers_empty():
    """Test getting all beers with empty database"""
    with patch('core.database.Database.fetch') as mock_fetch:
        mock_fetch.return_value = []
        response = client.get("/beers")
        assert response.status_code == 200
        assert len(response.json()) == 0

def test_get_tasks_empty():
    """Test getting running tasks when none are running"""
    with patch('app.main.running_tasks', new_callable=lambda: []) as mock_running_tasks:
        response = client.get("/tasks/running")
        assert response.status_code == 200
        assert response.json() == {"tasks": []}

def test_get_tasks_running():
    """Test getting running tasks when one is running"""
    with patch('app.main.running_tasks', new_callable=lambda: ["fake-task-id"]) as mock_running_tasks:
        response = client.get("/tasks/running")
        assert response.status_code == 200
        assert response.json() == {"tasks": ["fake-task-id"]}