from todo_app.data.item import Item


class ViewModel:
    def __init__(self, items: Item):
        self._items = items
    
    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return self.get_filtered_items("To Do")

    @property
    def doing_items(self):
        return self.get_filtered_items("Doing")

    @property
    def done_items(self):
        return self.get_filtered_items("Done")

    def get_filtered_items(self, status):
        return list(filter(lambda item: item.status == status, self._items))