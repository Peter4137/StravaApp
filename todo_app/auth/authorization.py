import functools
from flask_login import current_user
from todo_app.auth.user_role import UserRole

class AppAuthorization:

    @staticmethod
    def writer(func):
        @functools.wraps(func)
        def check_writer_auth(*args, **kwargs):
            user = current_user
            if current_user.is_anonymous or user.role != UserRole.Writer:
                return "You do not have the correct permissions to carry out this action", 403
            else:
                return func(*args, **kwargs)
        return check_writer_auth

    @staticmethod
    def reader(func):
        @functools.wraps(func)
        def check_reader_auth(*args, **kwargs):
            if current_user.is_anonymous:
                return "You do not have the correct permissions to view this page", 403
            else:
                return func(*args, **kwargs)
        return check_reader_auth