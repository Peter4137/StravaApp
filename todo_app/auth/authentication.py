import os
import requests
from flask_login import login_user
from flask import redirect

from todo_app.auth.user import User

class AppAuthentication:
    def __init__(self):
        self.client_id = os.environ.get('OAUTH_CLIENT_ID')
        self.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')

    @classmethod
    def authenticate(self):
         return redirect(f"https://github.com/login/oauth/authorize?client_id={self.client_id}")

    @classmethod
    def handle_login(self, code):
        access_token = self.get_access_token(code)
        user_info = self.get_user_info(access_token)
        user = User(user_info["id"])
        login_user(user)
        return

    def get_access_token(self, code):
        try:
            response = requests.post(
            "https://github.com/login/oauth/access_token", 
            params={
                "client_id": self.client_id, 
                "client_secret": self.client_secret, 
                "code": code},
            headers={"Accept": "application/json"})
            
            response.raise_for_status()
        except Exception:
            pass
        return response.json()["access_token"]

    def get_user_info(self, access_token):
        response = requests.get("https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"})
        return response.json()
