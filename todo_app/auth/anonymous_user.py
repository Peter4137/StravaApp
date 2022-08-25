from flask_login import AnonymousUserMixin
from todo_app.auth.user_role import UserRole


class AnonymousUser(AnonymousUserMixin):
    @property
    def role(self):
        return UserRole.Admin.value