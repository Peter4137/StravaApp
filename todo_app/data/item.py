from todo_app.data.status import Status

class Item:
    def __init__(self, id, name, status = Status.ToDo.value):
        self.id = id
        self.name = name
        self.status = status

    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status
        
    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name']) 
    
    @classmethod
    def from_mongo_item(cls, item):
        return cls(item["_id"], item["name"], item["status"])

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "status": self.status})
