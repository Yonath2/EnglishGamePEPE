from status import Status


class Enemy:
    def __init__(self, char):
        self.x = 0
        self.y = 0
        self.width = char.get_width()
        self.height = char.get_height()
        self.rect = (self.x, self.y, self.width, self.height)
        self.attributes = {"max_health": 0,
                           "current_health": 0,
                           "base_damage": 0,
                           "temporary_damage_bonus": 0,
                           "armor": 0,
                           "temporary_armor": 0,
                           "armor_enchantment": None,
                           "resistances": [],
                           "weaknesses": [],
                           "status": Status(),
                           "loot_table": []}
        self.char = char
        self.animations = {}
        self.anim_wait_list = []

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        self.get_attributes("status").update_status()

    def get_attributes(self, attribute=None):
        if attribute is None:
            return self.attributes
        else:
            try:
                return self.attributes[attribute]
            except KeyError:
                print(f"Error from Enemy.get_attributes: This attribute '{attribute}' does not exist")

    def set_attribute(self, attribute, value):
        if attribute == "status":
            print("Warning: To set the status, "
                  "use the get_attributes('status').set_status(status, state, level=0) command")
            return
        try:
            self.attributes[attribute] = value
        except KeyError:
            print(f"Error from Enemy.set_attribute: This attribute '{attribute}' does not exist")

    def set_attributes(self, *values):
        """
        les valeurs des attributs sont changées dans l'ordre des attribut dans self.attributes
        Si la nouvelle valeur de l'attribut est "NoV" (no value), l'attribut conserve sa valeur initiale
        """

        for index, attribute in enumerate(self.attributes):
            try:
                value = values[index]
            except IndexError:
                value = "NoV"
            """
            S'il manque des valeurs dans *values, le programme va remplacer les valeurs manquantes par des NoV
            (No value)
            """
            if not value == "NoV":
                self.set_attribute(attribute, values[index])

    """
    def get_status(self, status=None):
        if status is None:
            return self.attributes["status"].get_status()
        else:
            try:
                return self.attributes["status"].get_status(status)
            except:
                print("This status does not exist")
    """

    def set_animation(self, animation, new_state, speed, repeat=0):
        self.anim_wait_list.append((self.animations[animation], new_state, speed, repeat))

    def play_animation(self):
        if not self.anim_wait_list == []:
            anim_playing = self.anim_wait_list[0]
            animation = anim_playing[0]
            new_state = anim_playing[1]
            speed = anim_playing[2]
            repeat = anim_playing[3]
            playing = animation.play(new_state, speed, repeat)
            if playing != new_state:
                self.char = playing
            else:
                self.char = new_state
                animation.reset()
                self.anim_wait_list.pop(0)

    def attack(self):
        pass

    def draw(self, win):
        win.blit(self.char, (self.x, self.y))
