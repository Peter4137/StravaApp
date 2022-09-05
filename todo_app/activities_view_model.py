class ActivitiesViewModel:
    def __init__(self, activities):
        self._activities = activities

    @property
    def activities(self):
        return self._activities