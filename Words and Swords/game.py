import pygame
from player import Player
from bestiary import Bestiary
from background import Background
from words_and_synonyms import Words

pygame.init()

scr = [960, 720]

BACKGROUND_COLOR = (51, 57, 65)
LINES_COLOR = (146, 220, 190)

font_size = 50

constant = {"scr": scr[0] / scr[1],
            "font": font_size/scr[1],
            "enemy_separation": 0}

win = pygame.display.set_mode(scr, pygame.RESIZABLE)
pygame.display.set_caption("Words and Swords")

active_enemies = []


def add_active_enemy(enemy, pos=None):
    active_enemies.append(Bestiary.enemies[enemy])
    if pos is None:  # met la position en x selon le nombre d'ennemis et la position en y selon les pieds du joueur
        floor = constant["player_y_feet"]
        y = floor - Bestiary.enemies[enemy].get_height()
        x = 4*scr[0]/10 + sum([enemies.get_width() for enemies in active_enemies if enemies != Bestiary.enemies[enemy]]) # + constant["enemy_separation"] * len(active_enemies)
        x, y = x / scr[0] * 100, y / scr[1] * 100
        Bestiary.enemies[enemy].set_absolute_pos(x, y)
    else:
        Bestiary.enemies[enemy].set_absolute_pos(pos[0], pos[1])  # la position de l'enemi est en pourcentage de l'écran
    constant[Bestiary.enemies[enemy].get_name()] = Bestiary.enemies[enemy].get_width() / scr[0]
    Bestiary.enemies[enemy].load_animations()


def remove_active_enemy(enemy="all"):
    if enemy == "all":
        active_enemies.clear()
    else:
        active_enemies.remove(Bestiary.enemies[enemy])


def redrawGameWindow(win, command, player, enemies, font_ratio):
    font = pygame.font.Font("font/alagard.ttf", int(scr[1]*font_ratio))

    win.fill((255,255,255))

    Background.display_background(win)

    player.draw(win, scr)
    player.play_animation()

    for enemy in enemies:
        enemy.draw(win, scr)
        enemy.play_animation()

    text = font.render(command, 1, (255, 255, 255), (0, 0, 0))
    win.blit(text, (scr[0]/2 - text.get_width()/2, scr[1] - text.get_height()))

    pygame.display.flip()


def main():
    global win, scr, active_enemies, constant
    clock = pygame.time.Clock()

    # <Test>
    Bestiary.load_enemies()
    Background.load_backgrounds(scr[0], scr[1])

    p = Player(x=5, y=45, width=125, height=175, max_health=100)  # la position du personnage est en pourcentage de l'écran
    constant["player_scr_width"] = p.get_width() / scr[0]
    constant["player_y_feet"] = p.get_relative_pos(scr)[1] + p.get_height()
    p.load_animations()
    p.get_attributes("status").set_status("poisoned", True, level=1)
    p.get_attributes("status").update_status()

    Background.set_background_active("ui", 50)

    add_active_enemy("charcadonic_lizard_fire")
    add_active_enemy("slim_the_slimy_slime")
    print(Bestiary.enemies["charcadonic_lizard_fire"].get_absolute_pos(), constant["player_y_feet"], p.get_absolute_pos())
    print(Bestiary.enemies["slim_the_slimy_slime"].get_absolute_pos())
    # <\Test>

    active = False
    command = ''
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.VIDEORESIZE or win.get_width() != scr[0]:
                if event.size[0]/event.size[1] != constant["scr"]:
                    new_scr = (int(event.size[0]), int(event.size[0]*720/960))
                else:
                    new_scr = event.size
                p.set_new_size(new_scr, event.size, constant["player_scr_width"])
                win = pygame.display.set_mode(new_scr, pygame.RESIZABLE)
                scr = win.get_width(), win.get_height()
                Background.resize_active_background(scr[0], scr[1])
                for enemy in active_enemies:
                    enemy.set_new_size(new_scr, event.size, constant[enemy.get_name()])

            if event.type == pygame.FULLSCREEN:
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = not active
                if active:
                    if event.key == pygame.K_ESCAPE:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        command = command[:-1]
                    else:
                        command += event.unicode
                if event.key == pygame.K_p:
                    p.move()

        redrawGameWindow(win, command, p, active_enemies, constant["font"])


if __name__ == "__main__":
    main()
