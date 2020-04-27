class Inventory:
    def __init__(self):
        self.items = {"armors": [],
                      "melee weapons": [],
                      "range weapons": [],
                      "consumables": [],
                      "potions": []}
        self.artifacts = {}
        self.powers = {}

    def get_inventory(self):
        return self.items

    def get_category(self, name):
        try:
            category = self.items[name]
            return category
        except KeyError:
            print(f"Error from Inventory.get_category: this category '{name}' does not exist")

    def get_artifacts(self):
        return self.artifacts

    def get_powers(self):
        return self.powers



























