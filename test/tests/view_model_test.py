import pytest
from todo_app.data.item import Item
from todo_app.data.status import Status
from todo_app.user_view_model import ItemsViewModel
from todo_app.auth.user import User
from todo_app.auth.user_role import UserRole

@pytest.fixture
def view_model():
    return ItemsViewModel([
        Item(1, "To do item", Status.ToDo.value),
        Item(1, "Doing item", Status.Doing.value),
        Item(1, "Done item", Status.Done.value)
    ], User(1, UserRole.Admin, "Username"))

def test_to_do_items_in_separate_list(view_model: ItemsViewModel):
    assert len(view_model.to_do_items) == 1
    assert view_model.to_do_items[0].status == "To Do"

def test_doing_items_in_separate_list(view_model: ItemsViewModel):
    assert len(view_model.doing_items) == 1
    assert view_model.doing_items[0].status == "Doing"

def test_done_items_in_separate_list(view_model: ItemsViewModel):
    assert len(view_model.done_items) == 1
    assert view_model.done_items[0].status == "Done"



