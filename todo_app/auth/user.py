from re import U
from flask_login import UserMixin

from todo_app.auth.user_role import UserRole

class User(UserMixin):
    def __init__(self, id, role, name):
        self.id = id
        self.role = role
        self.name = name

    @classmethod
    def from_mongo_user(cls, user):
        return cls(int.from_bytes(user["_id"].binary, "little"), user["role"], user["name"])
