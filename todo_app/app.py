from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items, add_item as add_new_item, mark_item_as_complete, remove_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/", methods=["GET"])
def index():
    items = get_items()
    return render_template('index.html', items=items)

@app.route("/items/add", methods=["POST"])
def add_item():
    title = request.form.get("title")
    add_new_item(title)
    return redirect("/")


@app.route("/items/complete/<id>", methods=["POST"])
def complete(id):
    mark_item_as_complete(id)
    return redirect("/")

@app.route("/items/remove/<id>", methods=["POST"])
def remove(id):
    remove_item(id)
    return redirect("/")