from enemy import Enemy
from animation import Animation
import pygame, os


class Bestiary:
    enemies = {}

    @classmethod
    def load_enemies(cls):
        enemy_list = os.listdir("animations/enemies")
        for enemy in enemy_list:
            cls.enemies[enemy] = Enemy(pygame.image.load(f"animations/enemies/{enemy}/default/1.png"))
        # print(cls.enemies)

    @classmethod
    def load_animations(cls, name):
        load_frames = {}
        animations = {}
        animation_name = os.listdir(f"animations/enemies/{name}")
        for anims in animation_name:
            dir = os.listdir(f"animations/enemies/{name}/{anims}")
            load_frames[anims] = [pygame.image.load(f"animations/enemies/{name}/{anims}/{frame}") for frame in dir]
            animations[anims] = Animation(load_frames[anims])
        cls.enemies[name].animations = animations

    @classmethod
    def load_enemy(cls, name, x, y):
        cls.enemies[name].x = x
        cls.enemies[name].y = y

