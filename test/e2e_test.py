from multiprocessing.sharedctypes import Value
import pytest
import os
from threading import Thread
from todo_app import app
from dotenv import load_dotenv, find_dotenv
from todo_app.data.trello_items import TrelloItems
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv(".env")
    load_dotenv(file_path, override=True)

    trello_items = TrelloItems()
    board_id = trello_items.create_board("test1234")
    os.environ['TRELLO_BOARD_ID'] = board_id
    
    application = app.create_app()
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    thread.join(1)
    trello_items.delete_board(board_id)

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    with webdriver.Firefox(options = options) as driver:
        yield driver

def test_full_journey(driver, app_with_temp_board):
    """
    Test to check:
    - Hit index page
    - Create item
    - Move item to Doing
    - Move item to Done
    - Delete item
    """
    base_url = "http://localhost:5000/"
    driver.get(base_url)
    assert driver.title == 'To-Do App'

    add_item_input = driver.find_element(By.NAME, "title")
    add_item_input.send_keys("Test item")
    add_item_input.send_keys(Keys.RETURN)

    driver.implicitly_wait(2)
    assert driver.find_element(By.ID, "to-do-item")

    progress_button = driver.find_element(By.ID, "progress-button")
    progress_button.click()

    driver.implicitly_wait(2)
    assert driver.find_element(By.ID, "doing-item")

    progress_button = driver.find_element(By.ID, "progress-button")
    progress_button.click()

    driver.implicitly_wait(2)
    assert driver.find_element(By.ID, "done-item")

    delete_button = driver.find_element(By.ID, "delete-button")
    delete_button.click()

    with pytest.raises(NoSuchElementException):
        assert driver.find_element(By.ID, "done-item")





