
from todo_app.data.strava_user import StravaUser


class UserViewModel:
    def __init__(self, user: StravaUser):
        self._user = user
    
    @property
    def user(self):
        return self._user