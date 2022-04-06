from flask import Flask, render_template, request, redirect
from data.trello_items import TrelloItems
from view_model import ViewModel
from flask_config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trelloItems = TrelloItems()

    @app.route("/", methods=["GET"])
    def index():
        items = trelloItems.get_items()
        items_view_model = ViewModel(items)
        return render_template('index.html', view_model=items_view_model)

    @app.route("/items/add", methods=["POST"])
    def add_item():
        title = request.form.get("title")
        trelloItems.add_item(title)
        return redirect("/")


    @app.route("/items/progress/<id>", methods=["POST"])
    def progress(id):
        trelloItems.progress_item(id)
        return redirect("/")

    @app.route("/items/remove/<id>", methods=["POST"])
    def remove(id):
        trelloItems.remove_item(id)
        return redirect("/")

    return app