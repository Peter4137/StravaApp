class ActivitiesViewModel:
    def __init__(self, activities, vdot):
        self._activities = activities
        self._vdot = vdot

    @property
    def activities(self):
        return self._activities

    @property
    def vdot(self):
        return self._vdot