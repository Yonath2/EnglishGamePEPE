class Status:
    def __init__(self):
        self.status = {"poisoned": (False, 0),
                       "fire": (False, 0),
                       "strength": (False, 0),
                       "weakness": (False, 0)}

    def get_status(self, status=None):
        if status is None:
            return self.status
        else:
            try:
                return self.status[status]
            except KeyError:
                print(f"Error from Status.get_status: This status '{status}' does not exist")

    def set_status(self, status, state, level=0):  # state --> True ou False
        if not state == bool(state):
            print(f"Error from Status.set_status: State must be True or False, not '{state}'")
            return
        if status not in self.status:
            print(f"Error from Status.set_status: This status '{status}' does not exist")
            return
        self.status[status] = (state, level)

    def update_status(self):
        for status in self.status:
            if self.status[status][1] == 0:  # si le niveau du status est de 0, le status devient inactif
                self.set_status(status, False)
















