class Activity:
    def __init__(self, id, name, sport, date):
        self.id = id
        self.name = name
        self.sport = sport
        self.date = date
        
    @classmethod
    def from_strava_response(cls, activity):
        return cls(activity['id'], activity['name'], activity['sport_type'], activity['start_date'])

