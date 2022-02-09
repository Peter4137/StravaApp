import pytest
import os
import requests
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, "request", get_lists_stub)
    response = client.get("/")
    content = response.data.decode('utf8')
    assert "Test card" in content

class StubResponse():
    def __init__(self, fake_response_data, status):
        self.fake_response_data = fake_response_data
        self.status = status

    def json(self):
        return self.fake_response_data

    def raise_for_status(self):
        pass

def get_lists_stub(method, url, headers, params):
    test_board_id = os.environ.get("TRELLO_BOARD_ID")
    fake_response_data = None
    if url == f"https://api.trello.com/1/boards/{test_board_id}/lists":
        fake_response_data = [{
        "id": "123abc",
        "name": "To Do",
        "cards": [{"id": "456", "name": "Test card"}]
        }]
    return StubResponse(fake_response_data, 200)