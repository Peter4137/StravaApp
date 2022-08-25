import functools
import os
from flask_login import current_user
from todo_app.auth.user_role import UserRole

class AppAuthorization:

    # Hierarchy is Admin > Writer > Reader > Anonymous

    @staticmethod
    def admin(func):
        @functools.wraps(func)
        def check_admin_auth(*args, **kwargs):
            user = current_user
            if (current_user.is_anonymous or user.role != UserRole.Admin.value) and os.environ.get('LOGIN_DISABLED') == "False":
                return "You do not have the correct permissions to carry out this action", 403
            else:
                return func(*args, **kwargs)
        return check_admin_auth

    @staticmethod
    def writer(func):
        @functools.wraps(func)
        def check_writer_auth(*args, **kwargs):
            user = current_user
            if (current_user.is_anonymous or user.role == UserRole.Reader.value) and os.environ.get('LOGIN_DISABLED') == "False":
                return "You do not have the correct permissions to carry out this action", 403
            else:
                return func(*args, **kwargs)
        return check_writer_auth

    @staticmethod
    def reader(func):
        @functools.wraps(func)
        def check_reader_auth(*args, **kwargs):
            if current_user.is_anonymous and os.environ.get('LOGIN_DISABLED') == "False":
                return "You do not have the correct permissions to view this page", 403
            else:
                return func(*args, **kwargs)
        return check_reader_auth