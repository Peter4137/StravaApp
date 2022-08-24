import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED') == "True"

        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")