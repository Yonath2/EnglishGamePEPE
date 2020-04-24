import pygame, os
from animation import Animation


class Background:
    backgrounds = {}
    active_bg = None

    @classmethod
    def load_backgrounds(cls, width, height, name=None):
        if name is None:
            bg_list = os.listdir("backgrounds")
            for bg in bg_list:
                dir = os.listdir(f"backgrounds/{bg}")
                frames = [pygame.image.load(f"backgrounds/{bg}/{frame}") for frame in dir]
                cls.backgrounds[bg] = [pygame.transform.scale(frames[frame], (width, height)) for frame in range(len(frames))]
        else:
            dir = os.listdir(f"backgrounds/{name}")
            frames = [pygame.image.load(f"backgrounds/{name}/{frame}") for frame in dir]
            cls.backgrounds[name] = [pygame.transform.scale(frames[frame], (width, height)) for frame in range(len(frames))]

    @classmethod
    def set_background_active(cls, name, speed):
        try:
            cls.active_bg = (Animation(cls.backgrounds[name]), name, speed)
        except KeyError:
            print(f"Error from set_background_active: This name '{name}' is not the name of a background")

    @classmethod
    def display_background(cls, win):
        frame = None
        if cls.active_bg is not None:
            frame = cls.active_bg[0].play(cls.active_bg[0].frames[0], cls.active_bg[2], -1)
            win.blit(frame, (0, 0))

    @classmethod
    def resize_active_background(cls, width, height):
        for background in cls.backgrounds:
            if background == cls.active_bg[1]:
                cls.load_backgrounds(width, height, background)
                frames = cls.backgrounds[background]
                cls.backgrounds[background] = [pygame.transform.scale(frames[frame], (width, height)) for frame in range(len(frames))]
                cls.set_background_active(background, cls.active_bg[2])



















