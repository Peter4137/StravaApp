class StravaUser:
    def __init__(self, id, firstname, lastname):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname

    @classmethod
    def from_strava_response(cls, user):
        return cls(user['id'], user['firstname'], user['lastname'])