import pytest
from todo_app.data.item import Item
from todo_app.data.status import Status
from todo_app.view_model import ViewModel


@pytest.fixture
def view_model():
    return ViewModel([
        Item(1, "To do item", Status.ToDo.value),
        Item(1, "Doing item", Status.Doing.value),
        Item(1, "Done item", Status.Done.value)
    ])

def test_to_do_items_in_separate_list(view_model: ViewModel):
    assert len(view_model.to_do_items) == 1
    assert view_model.to_do_items[0].status == "To Do"

def test_doing_items_in_separate_list(view_model: ViewModel):
    assert len(view_model.doing_items) == 1
    assert view_model.doing_items[0].status == "Doing"

def test_done_items_in_separate_list(view_model: ViewModel):
    assert len(view_model.done_items) == 1
    assert view_model.done_items[0].status == "Done"



