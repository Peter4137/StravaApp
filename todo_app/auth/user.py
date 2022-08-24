from re import U
from flask_login import UserMixin

from todo_app.auth.user_role import UserRole

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        if int(id) == 17096633:
            self.role = UserRole.Writer
        else:
            self.role = UserRole.Reader