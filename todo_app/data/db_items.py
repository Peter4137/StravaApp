import os
import pymongo
from bson.objectid import ObjectId

from todo_app.data.item import Item
from todo_app.data.list import List
from todo_app.data.status import Status

class DatabaseItems:

    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.environ.get('DATABASE_CONNECTION_STRING'))
        self.db = self.client[os.environ.get('DATABASE_NAME')]
        self.items = self.db.items

    def get_items(self):
        """
        Fetches all saved items from trello.

        Returns:
            list: The list of saved items.
        """
        items = self.items.find()
        parsed_items = [Item.from_mongo_item(item) for item in items]
        return sorted(parsed_items, key=lambda item: item.id)

    def get_item(self, id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        item = self.items.find_one({"_id": ObjectId(id)})
        return Item.from_mongo_item(item)

    def add_item(self, title):
        """
        Adds a new item with the specified title to the session.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        item = {
            "name": title,
            "status": Status.ToDo.value
        }
        self.items.insert_one(item)

    def progress_item(self, id):
        """
        Progresses an existing item one step (To do -> Doing -> Done). If no existing item matches the ID of the specified item, nothing is marked as done

        Args:
            id: The ID of the item to progress 
        """
        next_status = Status.get_next(self.get_item(id).status)
        self.items.update_one({"_id": ObjectId(id)}, {"$set": {"status": next_status.value}})

    def remove_item(self, id):
        """
        Removes an existing item from the board. If no existing item matches the ID of the specified item, no item is removed

        Args:
            id: The ID of the item to remove
        """
        self.items.delete_one({"_id": ObjectId(id)})

    def clear_all(self):
        """
        Removes the items collection from the database, effectively clearing all items
        """
        self.items.drop()
