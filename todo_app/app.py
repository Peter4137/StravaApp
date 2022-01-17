from flask import Flask, render_template, request, redirect
from todo_app.data.trello_items import get_items, add_item as add_new_item, progress_item, remove_item
from todo_app.view_model import ViewModel
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/", methods=["GET"])
def index():
    items = get_items()
    items_view_model = ViewModel(items)
    return render_template('index.html', view_model=items_view_model)

@app.route("/items/add", methods=["POST"])
def add_item():
    title = request.form.get("title")
    add_new_item(title)
    return redirect("/")


@app.route("/items/progress/<id>", methods=["POST"])
def progress(id):
    progress_item(id)
    return redirect("/")

@app.route("/items/remove/<id>", methods=["POST"])
def remove(id):
    remove_item(id)
    return redirect("/")