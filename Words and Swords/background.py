import pygame, os
from animation import Animation


class Background:
    backgrounds = {}
    active_bg = None

    @classmethod
    def load_backgrounds(cls):
        bg_list = os.listdir("backgrounds")
        for bg in bg_list:
            dir = os.listdir(f"backgrounds/{bg}")
            cls.backgrounds[bg] = [pygame.image.load(f"backgrounds/{bg}/{frame}") for frame in dir]

    @classmethod
    def set_background_active(cls, name):
        try:
            cls.active_bg = Animation(cls.backgrounds[name])
        except KeyError:
            print(f"Error from set_background_active: This name '{name}' is not the name of a background")

    @classmethod
    def display_background(cls, win):
        frame = None
        if cls.active_bg is not None:
            frame = cls.active_bg.play(cls.active_bg.frames[0], 10, -1)
            win.blit(frame, (0, 0))

    @classmethod
    def resize_backgrounds(cls, width, height, name=None):
        if name is None:
            for background in cls.backgrounds:
                cls.backgrounds[background] = pygame.transform.scale(frame, (width, height))
        else:
            pass




















