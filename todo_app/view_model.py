from todo_app.data.item import Item
from todo_app.auth.user import User
from todo_app.auth.user_role import UserRole


class ViewModel:
    def __init__(self, items: Item, user: User):
        self._items = items
        self._user = user
    
    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return self.get_filtered_items("To Do")

    @property
    def doing_items(self):
        return self.get_filtered_items("Doing")

    @property
    def done_items(self):
        return self.get_filtered_items("Done")

    @property
    def is_writer(self):
        return self._user.role == UserRole.Writer

    def get_filtered_items(self, status):
        return list(filter(lambda item: item.status == status, self._items))