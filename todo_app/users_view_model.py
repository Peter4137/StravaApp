from todo_app.data.item import Item
from todo_app.auth.user import User
from todo_app.auth.user_role import UserRole


class UsersViewModel:
    def __init__(self, users):
        self._users = users
    
    @property
    def users(self):
        return self._users