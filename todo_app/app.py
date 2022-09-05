from cProfile import run
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required
from matplotlib import pyplot as plt
import matplotlib
import mpld3

from todo_app.activities_view_model import ActivitiesViewModel
from todo_app.data.strava_client import StravaClient
from todo_app.data.strava_user import StravaUser
from todo_app.flask_config import Config
from todo_app.auth.user import User
from todo_app.auth.authentication import AppAuthentication
from todo_app.auth.anonymous_user import AnonymousUser
from todo_app.user_view_model import UserViewModel
from todo_app.data.running_calculator import RunningCalculator

matplotlib.use('Agg')

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config())
    

    login_manager = LoginManager()
    login_manager.anonymous_user = AnonymousUser
    app_authentication = AppAuthentication()

    running_calculator = RunningCalculator()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return app_authentication.authenticate()

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    strava_client = StravaClient()

    @app.route("/", methods=["GET"])
    @login_required
    def index():
        activities = strava_client.get_activities()
        activities_view_model = ActivitiesViewModel(activities)
        return render_template('activities.html', view_model=activities_view_model)

    @app.route("/activity/<id>", methods=["GET"])
    @login_required
    def activity(id):
        plt_html = running_calculator.plot_session(id)
        return render_template('plot.html', figure=plt_html)

    @app.route("/performance", methods=["GET"])
    @login_required
    def performance():
        sessions = strava_client.get_activities()
        running_ids = []
        for session in sessions:
            if session.sport == 'Run':
                running_ids.append(session.id)
        plt_html = running_calculator.plot_sessions(running_ids)
        return render_template('plot.html', figure=plt_html)

    # @app.route("/items/add", methods=["POST"])
    # @login_required
    # @AppAuthorization.writer
    # def add_item():
    #     title = request.form.get("title")
    #     databaseItems.add_item(title)
    #     return redirect("/")

    @app.route("/login/callback", methods=["GET"])
    def login_callback():
        code = request.args.get("code")
        app_authentication.handle_login(code)
        return redirect("/")

    return app


