import pytest
import os
from dotenv import load_dotenv, find_dotenv
from bson.objectid import ObjectId
import mongomock
import pymongo

from todo_app import app
from todo_app.data.status import Status
from todo_app.auth.user_role import UserRole

@pytest.fixture
def client():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)


    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    test_name = "Test card"
    items = pymongo.MongoClient(os.environ.get('DATABASE_CONNECTION_STRING'))[os.environ.get('DATABASE_NAME')].items
    response = items.insert_one({"name": test_name, "status": Status.ToDo.value})
    response = client.get("/")
    content = response.data.decode('utf8')
    assert test_name in content

def test_users_page(client):
    test_name = "Test name"
    users = pymongo.MongoClient(os.environ.get('DATABASE_CONNECTION_STRING'))[os.environ.get('DATABASE_NAME')].users
    response = users.insert_one({"_id": ObjectId(), "role": UserRole.Admin.value, "name": test_name})
    response = client.get("/users")
    content = response.data.decode('utf8')
    assert test_name in content