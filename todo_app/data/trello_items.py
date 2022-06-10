import os
import requests
import itertools

from todo_app.data.item import Item
from todo_app.data.list import List
from todo_app.data.status import Status

class TrelloItems:

    def __init__(self) -> None:
        self.trello_base_url = "https://api.trello.com" 
        self.api_key = os.environ.get("TRELLO_API_KEY")
        self.api_token = os.environ.get('TRELLO_TOKEN')
        self.board_id = os.environ.get('TRELLO_BOARD_ID')
        self.organization_id = os.environ.get('TRELLO_ORGANIZATION_ID')

    def trello_request(self, method, path, query_params = {}):
        headers = {
            "Accept": "application/json"
        }
        query_params["key"] = self.api_key
        query_params["token"] = self.api_token
        url = f"{self.trello_base_url}{path}"

        response = requests.request(
            method,
            url,
            headers=headers,
            params=query_params
        )
        response.raise_for_status()

        return response.json()

    def get_items(self):
        """
        Fetches all saved items from trello.

        Returns:
            list: The list of saved items.
        """
        def parse_column(column):
            return [Item.from_trello_card(card, column) for card in column["cards"]]
        
        response = self.trello_request("GET", f"/1/boards/{self.board_id}/lists", {"cards": "open"})

        return sorted(list(itertools.chain(*[parse_column(col) for col in response])), key=lambda item: item.id)

    def get_item(self, id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item.id == id), None)

    def get_lists(self):
        """
        Gets all the lists for the trello board

        Returns:
            lists: a list of List objects
        """
        response = self.trello_request("GET", f"/1/boards/{self.board_id}/lists")
        return [List.from_trello_list(trello_list) for trello_list in response]

    def get_list_id_from_name(self, status_name: Status):
        """
        Gets the trello list id of a list with the given name, or None if it does not exist
        
        Args:
            name: The name of the list.

        Returns:
            listId: the id of the list, or None if it does not exist 
        """
        trello_lists = self.get_lists()
        return next((trello_list.id for trello_list in trello_lists if trello_list.name ==status_name.value), None)

    def add_item(self, title):
        """
        Adds a new item with the specified title to the session.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """

        todo_id = self.get_list_id_from_name(Status.ToDo)
        self.trello_request("POST", f"/1/cards", {"idList": todo_id, "name": title})

    def progress_item(self, id):
        """
        Progresses an existing item one step (To do -> Doing -> Done). If no existing item matches the ID of the specified item, nothing is marked as done

        Args:
            id: The ID of the item to progress 
        """
        next_status = Status.get_next(self.get_item(id).status)
        status_id = self.get_list_id_from_name(next_status)
        self.trello_request("PUT", f"/1/cards/{id}", {"idList": status_id})

    def remove_item(self, id):
        """
        Removes an existing item from the board. If no existing item matches the ID of the specified item, no item is removed

        Args:
            id: The ID of the item to remove
        """
        self.trello_request("DELETE", f"/1/cards/{id}")


    def create_board(self, name):
        """
        Creates a new board in trello
        """

        response = self.trello_request("POST", f"/1/boards", {"name": name, "idOrganization": self.organization_id})
        return response["id"]

    def delete_board(self, id):
        """ 
        Deletes the board with the given ID
        """

        self.trello_request("DELETE", f"/1/boards/{id}")
