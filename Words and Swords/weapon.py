class Weapon:
    def __init__(self, image):
        self.image = image
        self.attributes = {"type": None,
                           "base_damage": 0,
                           "damage_type": None,
                           "element": None}

    def get_attributes(self, attribute=None):
        if attribute is None:
            return self.attributes
        else:
            try:
                return self.attributes[attribute]
            except KeyError:
                print(f"Error from Weapon.get_attributes: This attribute '{attribute}' does not exist")

    def set_attribute(self, attribute, value):
        try:
            self.attributes[attribute] = value
        except KeyError:
            print(f"Error from Weapon.set_attribute: This attribute '{attribute}' does not exist")








