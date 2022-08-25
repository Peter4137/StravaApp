from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user, logout_user

from todo_app.data.db_items import DatabaseItems
from todo_app.data.db_users import DatabaseUsers
from todo_app.items_view_model import ItemsViewModel
from todo_app.users_view_model import UsersViewModel
from todo_app.flask_config import Config
from todo_app.auth.user import User
from todo_app.auth.authorization import AppAuthorization
from todo_app.auth.authentication import AppAuthentication

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    login_manager = LoginManager()
    app_authentication = AppAuthentication()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return app_authentication.authenticate()

    @login_manager.user_loader
    def load_user(user_id):
        return databaseUsers.get_user(int(user_id))

    login_manager.init_app(app)

    databaseItems = DatabaseItems()
    databaseUsers = DatabaseUsers()

    @app.route("/", methods=["GET"])
    @login_required
    @AppAuthorization.reader
    def index():
        items = databaseItems.get_items()
        items_view_model = ItemsViewModel(items, current_user)
        return render_template('index.html', view_model=items_view_model)

    @app.route("/items/add", methods=["POST"])
    @login_required
    @AppAuthorization.writer
    def add_item():
        title = request.form.get("title")
        databaseItems.add_item(title)
        return redirect("/")

    @app.route("/items/progress/<id>", methods=["POST"])
    @login_required
    @AppAuthorization.writer
    def progress(id):
        databaseItems.progress_item(id)
        return redirect("/")

    @app.route("/items/remove/<id>", methods=["POST"])
    @login_required
    @AppAuthorization.writer
    def remove(id):
        databaseItems.remove_item(id)
        return redirect("/")

    @app.route("/login/callback", methods=["GET"])
    def login_callback():
        code = request.args.get("code")
        app_authentication.handle_login(code)
        return redirect("/")

    @app.route("/logout", methods=["POST"])
    def logout():
        logout_user()
        return redirect("/")

    @app.route("/users", methods=["GET"])
    @login_required
    @AppAuthorization.admin
    def get_users():
        users = databaseUsers.get_users()
        users_view_model = UsersViewModel(users)
        return render_template('users.html', view_model=users_view_model)

    @app.route("/users/<id>/<role>", methods=["POST"])
    @login_required
    @AppAuthorization.admin
    def update_user_role(id, role):
        databaseUsers.update_user_role(id, role)
        return redirect("/users")

    return app


