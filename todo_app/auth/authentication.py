import os
import requests
from flask_login import login_user, logout_user, current_user
from flask import redirect, session

from todo_app.auth.user import User

class AppAuthentication:
    def __init__(self):
        self.client_id = os.environ.get('OAUTH_CLIENT_ID')
        self.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')
        self.redirect_url = os.environ.get('APP_URL')
        self.login_disabled = os.environ.get('LOGIN_DISABLED') == "True"

    def authenticate(self):
        return redirect(f"https://www.strava.com/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_url}/login/callback&response_type=code&scope=activity:read_all")

    def handle_login(self, code):
        token_response = self.exchange_token(code)
        athlete = token_response["athlete"]
        access_token = token_response["access_token"]
        session['access_token'] = access_token
        user = User(str(athlete['id']))
        login_user(user)

    def exchange_token(self, code):
        try:
            response = requests.post(
            "https://www.strava.com/oauth/token", 
            params={
                "client_id": self.client_id, 
                "client_secret": self.client_secret, 
                "code": code,
                "grant_type": "authorization_code"},
            headers={"Accept": "application/json"})
            
            response.raise_for_status()
        except Exception:
            logout_user()
            return
        return response.json()

    def get_user_info(self, access_token):
        response = requests.get("https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"})
        return response.json()
