import pygame, os
from status import Status
from inventory import Inventory
from animation import Animation


class Player:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.default_char = pygame.image.load("animations/player/default/1.png")
        self.char = self.default_char
        self.rect = (x, y, width, height)
        self.attributes = {"max_health": max_health,
                           "current_health": max_health,
                           "base_damage": 0,
                           "temporary_attack_bonus": 0,
                           "attack_bonus_multiplier": 0,  # nombre par lequel est multiplié le nombre de synonymes pour déterminer le bonus d'attaque
                           "armor": 0,
                           "temporary_armor_bonus": 0,
                           "armor_enchantment": None,
                           "status": Status(),
                           "inventory": Inventory()}
        self.load_frames = {}
        self.animations = {}
        self.anim_wait_list = []

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def load_animations(self, width=None, height=None):
        animation_name = os.listdir("animations/player")
        self.default_char = pygame.image.load("animations/player/default/1.png")
        if width is None or height is None:
            width = self.get_width()
            height = self.get_height()
        self.default_char = pygame.transform.scale(self.default_char, (width, height))
        self.char = self.default_char
        for name in animation_name:
            dir = os.listdir(f"animations/player/{name}")
            frames = [pygame.image.load(f"animations/player/{name}/{frame}") for frame in dir]
            self.load_frames[name] = [pygame.transform.scale(frame, (width, height)) for frame in frames]
            self.animations[name] = Animation(self.load_frames[name])

    def set_new_size(self, new_scr, size, scr_width_ratio):
        ratio = self.get_width()/self.get_height()
        if self.get_width() / size[1] != scr_width_ratio:
            new_p_width = int(new_scr[0] * scr_width_ratio)
            new_p_height = int(new_p_width * ratio ** -1)
        else:
            new_p_width = int((self.get_width() ** 3 * new_scr) / (scr_width_ratio / self.get_width()) ** -1)
            new_p_height = int(new_p_width * ratio ** -1)
        self.load_animations(width=new_p_width, height=new_p_height)

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
                print(f"Error from Player.get_attributes: This attribute '{attribute}' does not exist")

    def set_attribute(self, attribute, value):
        if attribute == "status":
            print("Warning: To set the status, "
                  "use the get_attributes('status').set_status(status, state, level=0) command")
            return
        try:
            self.attributes[attribute] = value
        except KeyError:
            print(f"Error from Player.set_attribute: This attribute '{attribute}' does not exist")



    """
    def get_status(self, status=None):
        if status is None:
            return self.attributes["status"]
        else:
            try:
                return self.attributes["status"].get_status(status)
            except:
                print("This status does not exist")
    """

    def move(self):
        self.set_animation("walk_right", self.default_char, 10, repeat=0)
        self.set_animation("walk_left", self.default_char, 10, repeat=0)
        self.set_animation("read", self.default_char, 10)

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

    def defense(self):
        pass

    def draw(self, win, scr):
        #pygame.draw.rect(win, (0, 255, 255), self.rect)
        win.blit(self.char, (self.x/100 * scr[0], self.y/100 * scr[1]))
