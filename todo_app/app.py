from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required

from todo_app.data.db_items import DatabaseItems
from todo_app.view_model import ViewModel
from todo_app.flask_config import Config
from todo_app.auth import AppAuth
from todo_app.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    login_manager = LoginManager()
    app_auth = AppAuth()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return app_auth.authenticate()

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    databaseItems = DatabaseItems()

    @login_required
    @app.route("/", methods=["GET"])
    def index():
        items = databaseItems.get_items()
        items_view_model = ViewModel(items)
        return render_template('index.html', view_model=items_view_model)

    @app.route("/items/add", methods=["POST"])
    @login_required
    def add_item():
        title = request.form.get("title")
        databaseItems.add_item(title)
        return redirect("/")

    @app.route("/items/progress/<id>", methods=["POST"])
    @login_required
    def progress(id):
        databaseItems.progress_item(id)
        return redirect("/")

    @app.route("/items/remove/<id>", methods=["POST"])
    @login_required
    def remove(id):
        databaseItems.remove_item(id)
        return redirect("/")

    @app.route("/login/callback", methods=["GET"])
    def login_callback():
        code = request.args.get("code")
        app_auth.handle_login(code)
        return redirect("/")

    return app