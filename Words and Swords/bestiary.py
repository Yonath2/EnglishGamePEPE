from enemy import Enemy
from animation import Animation
import pygame, os


class Bestiary:
    enemies = {}

    @classmethod
    def load_enemies(cls):
        enemy_list = os.listdir("animations/enemies")
        for enemy in enemy_list:
            cls.enemies[enemy] = Enemy(pygame.image.load(f"animations/enemies/{enemy}/default/1.png"), enemy)
        # print(cls.enemies)

