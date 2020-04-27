class Armor:
    def __init__(self, image):
        self.image = image
        self.attributes = {"armor": 0,
                           "enchantment": None}  # name: value

    def get_attributes(self, attribute=None):
        if attribute is None:
            return self.attributes
        else:
            try:
                return self.attributes[attribute]
            except KeyError:
                print(f"Error from Armor.get_attributes: This attribute '{attribute}' does not exist")

    def set_attribute(self, attribute, value):
        try:
            self.attributes[attribute] = value
        except KeyError:
            print(f"Error from Armor.set_attribute: This attribute '{attribute}' does not exist")











