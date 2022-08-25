from enum import Enum

class UserRole(Enum):
    Reader = "Reader"
    Writer = "Writer"
    Admin = "Admin"