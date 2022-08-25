import os
import pymongo
from bson.objectid import ObjectId

from todo_app.auth.user import User
from todo_app.auth.user_role import UserRole
from todo_app.data.status import Status

class DatabaseUsers:

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.environ.get('DATABASE_CONNECTION_STRING'))
        self.db = self.client[os.environ.get('DATABASE_NAME')]
        self.users = self.db.users

    def add_user_if_new(self, id, name):
        user = self.users.find_one({"_id": ObjectId(id.to_bytes(12, "little"))})
        if user is None:
            return self.add_user(id, name)
        else:
            return User.from_mongo_user(user)

    def add_user(self, id, name):
        if self.admin_exists():
            role = UserRole.Reader
        else:
            role = UserRole.Admin
        id_bytes = id.to_bytes(12, "little")
        user = {
            "_id": ObjectId(id_bytes),
            "role": role.value,
            "name": name
        }
        self.users.insert_one(user)
        return User.from_mongo_user(user)

    def admin_exists(self):
        return self.users.count_documents({"role": UserRole.Admin.value}) != 0

    def update_user_role(self, id, role):
        if (role not in [role.value.lower() for role in UserRole]):
            raise ValueError(f"{role} is not a recognised user role")
        self.users.update_one({"_id": ObjectId(id)}, {"$set": {"role": role}})

    def get_users(self):
        users = self.users.find()
        parsed_users = [User.from_mongo_user(user) for user in users]
        return sorted(parsed_users, key=lambda user: user.name)

    def get_user(self, id):
        user = self.users.find_one({"_id": ObjectId(id.to_bytes(12, "little"))})
        return User.from_mongo_user(user)