from enum import Enum
from os import environ

class Status(Enum):
    ToDo = "To Do"
    Doing = "Doing"
    Done = "Done"

    @staticmethod
    def get_next(enum):
        if enum == Status.ToDo.value:
            return Status.Doing
        else:
            return Status.Done