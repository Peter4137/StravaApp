import pytest
import os
import time
from threading import Thread
from todo_app import app
from dotenv import load_dotenv, find_dotenv
from todo_app.auth.user_role import UserRole
from todo_app.auth.user import User
from todo_app.data import db_users
from todo_app.data.db_items import DatabaseItems
from todo_app.data.db_users import DatabaseUsers
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

TEST_USER_ID = 1
TEST_USER_NAME = "Admin User"
SECOND_USER_ID = 2
SECOND_USER_NAME = "Second Name"

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv(".env")
    load_dotenv(file_path, override=True)
    os.environ['DATABASE_NAME'] = "test-database"
    os.environ['LOGIN_DISABLED'] = "True"

    db_items = DatabaseItems()
    db_users = DatabaseUsers()
    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    time.sleep(1)
    yield application

    thread.join(1)
    db_items.clear_all()
    db_users.clear_all()
    db_users.add_user(TEST_USER_ID, TEST_USER_NAME)
    db_users.add_user(SECOND_USER_ID, SECOND_USER_NAME)

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.headless = False
    with webdriver.Firefox(options = options) as driver:
        yield driver

def test_full_item_journey(driver, app_with_temp_board):
    """
    Test to check:
    - Hit index page
    - Create item
    - Move item to Doing
    - Move item to Done
    - Delete item
    """
    base_url = "http://localhost:5000/"
    driver.implicitly_wait(5)

    # Set user as admin to be able to edit page
    driver.get(base_url + "login/callback?code=1")

    driver.get(base_url)
    assert driver.title == 'To-Do App'

    add_item_input = driver.find_element(By.NAME, "title")
    add_item_input.send_keys("E2E Test item")
    add_item_input.send_keys(Keys.RETURN)

    assert driver.find_element(By.ID, "to-do-item")

    progress_button = driver.find_element(By.ID, "progress-button")
    progress_button.click()

    assert driver.find_element(By.ID, "doing-item")

    progress_button = driver.find_element(By.ID, "progress-button")
    progress_button.click()

    assert driver.find_element(By.ID, "done-item")

    delete_button = driver.find_element(By.ID, "delete-button")
    delete_button.click()

    with pytest.raises(NoSuchElementException):
        assert driver.find_element(By.ID, "done-item")

    

def test_user_update_journey(driver, app_with_temp_board):
    """
    Test to check:
    - Go to users page
    - Set Reader user as Writer
    - Return to index page
    """
    base_url = "http://localhost:5000/"
    driver.implicitly_wait(5)

    # Set user as admin so that users page button is shown
    driver.get(base_url + "login/callback?code=1")

    driver.get(base_url)
    users_page_button = driver.find_element(By.ID, "users-button")
    users_page_button.click()

    second_user_row = driver.find_element(By.ID, f"user-row-{SECOND_USER_ID}")
    assert second_user_row.find_element(By.ID, "user-role").text == "Reader"
    second_user_writer_button = second_user_row.find_element(By.ID, "writer-button")
    second_user_writer_button.click()

    second_user_row = driver.find_element(By.ID, f"user-row-{SECOND_USER_ID}")
    assert second_user_row.find_element(By.ID, "user-role").text == "Writer"

    items_page_button = driver.find_element(By.ID, "index-button")
    items_page_button.click()







