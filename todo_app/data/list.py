class List:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
    @classmethod
    def from_trello_list(cls, list):
        return cls(list['id'], list['name'])

