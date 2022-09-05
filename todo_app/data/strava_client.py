from flask import session
import requests

from todo_app.data.activity import Activity

class StravaClient:

    def __init__(self) -> None:
        return

    def strava_request(self, method, path, params={}):
        headers = {
            "Authorization": f"Bearer {session.get('access_token')}"
            }
        url = f"https://www.strava.com/api/v3/{path}"
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params
        )
        response.raise_for_status()

        return response.json()

    def get_user(self):
        return self.strava_request('GET', 'athlete')

    def get_activities(self):
        activities = self.strava_request('GET', 'athlete/activities', {"per_page": 50})
        return [Activity.from_strava_response(activity) for activity in activities]

    def get_activity_streams(self, id):
        params = {
            "keys": "velocity_smooth,time",
            "key_by_type": True
        }
        return self.strava_request('GET', f'activities/{id}/streams', params)

    def get_activity_laps(self, id):
        return self.strava_request('GET', f'activities/{id}/laps')
    