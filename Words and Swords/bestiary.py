from enemy import Enemy
from animation import Animation
import pygame, os


class Bestiary:
    enemies = {}

    @classmethod
    def load_enemies(cls, name=None):
        enemy_list = os.listdir("animations/enemies")
        if name is None:
            for enemy in enemy_list:
                cls.enemies[enemy] = Enemy(pygame.image.load(f"animations/enemies/{enemy}/idle/1.png"), enemy)
        else:
            try:
                cls.enemies[name] = Enemy(pygame.image.load(f"animations/enemies/{name}/idle/1.png"), name)
            except:
                print(f"Error from Bestiary.load_enemies: the enemy '{name}' does not exist")
        # print(cls.enemies)




