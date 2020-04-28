from status import Status
from animation import Animation
import os, pygame


class Enemy:
    def __init__(self, char, name):
        self.x = 0
        self.y = 0
        self.width = char.get_width()
        self.height = char.get_height()
        self.current_width = self.width
        self.current_height = self.height
        self.name = name
        self.rect = (self.x, self.y, self.width, self.height)
        self.attributes = {"max_health": 0,
                           "current_health": 0,
                           "initiative": 0,  # nombre qui indique l'ordre des tours; celui qui a la plus grande commence, puis, c'est au deuxième plus grand, etc.
                           "base_damage": 0,
                           "temporary_damage_bonus": 0,
                           "armor": 0,
                           "temporary_armor": 0,
                           "armor_enchantment": None,
                           "resistances": [],
                           "weaknesses": [],
                           "status": Status(),
                           "loot_table": []}
        self.default_char = char
        self.char = self.default_char
        self.load_frames = {}
        self.animations = {}
        self.anim_wait_list = []

    def get_name(self):
        return self.name

    def get_width(self, current=False):
        if not current:
            return self.width
        else:
            return self.current_width

    def get_height(self, current=False):
        if not current:
            return self.height
        else:
            return self.current_height

    def load_animations(self, width=None, height=None):
        self.default_char = pygame.image.load(f"animations/enemies/{self.get_name()}/idle/1.png")
        animation_name = os.listdir(f"animations/enemies/{self.get_name()}")
        if width is None or height is None:
            width = self.get_width()
            height = self.get_height()
        self.default_char = pygame.transform.scale(self.default_char, (width, height))
        self.char = self.default_char
        for anims in animation_name:
            dir = os.listdir(f"animations/enemies/{self.get_name()}/{anims}")
            frames = [pygame.image.load(f"animations/enemies/{self.get_name()}/{anims}/{frame}") for frame in dir]
            self.load_frames[anims] = [pygame.transform.scale(frame, (width, height)) for frame in frames]
            self.animations[anims] = Animation(self.load_frames[anims])

    def set_new_size(self, new_scr, size, scr_width_ratio):
        ratio = self.get_width() / self.get_height()
        if self.get_width() / size[1] != scr_width_ratio:
            new_e_width = int(new_scr[0] * scr_width_ratio)
            new_e_height = int(new_e_width * ratio ** -1)
        else:
            new_e_width = int((self.get_width() ** 3 * new_scr) / (scr_width_ratio / self.get_width()) ** -1)
            new_e_height = int(new_e_width * ratio ** -1)
        self.load_animations(width=new_e_width, height=new_e_height)
        self.current_width, self.current_height = new_e_width, new_e_height

    def set_absolute_pos(self, x, y):
        self.x = x
        self.y = y

    def get_absolute_pos(self):
        return self.x, self.y

    def get_relative_pos(self, scr):
        rx = self.x / 100 * scr[0]
        ry = self.y / 100 * scr[1]
        return rx, ry

    def update(self):
        self.rect = (self.x, self.y, self.get_width(), self.get_height())
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
        try:
            self.anim_wait_list.append((self.animations[animation], new_state, speed, repeat))
        except KeyError:
            print(f"Error from Enemy.set_animation: this animation '{animation}' does not exist")

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
                self.animations["idle"].reset()  # reset idle animation
        else:
            # idle animation
            self.char = self.animations["idle"].play(self.default_char, 100, repeat=-1)

    def attack(self):
        pass

    def draw(self, win, scr):
        win.blit(self.char, (self.get_relative_pos(scr)[0], self.get_relative_pos(scr)[1]))
