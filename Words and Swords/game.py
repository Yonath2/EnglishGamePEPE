import pygame
from player import Player
from bestiary import Bestiary
from background import Background
from words_and_synonyms import Words

pygame.init()

scr = [960, 720]

ratios = {"scr": scr[0]/scr[1]}

win = pygame.display.set_mode(scr, pygame.RESIZABLE)
pygame.display.set_caption("Words and Swords")

active_enemies = []

def redrawGameWindow(win, command, player, enemies):
    font = pygame.font.SysFont("times new roman", 40)

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


def add_active_enemy(enemy, x, y):
    active_enemies.append(Bestiary.enemies[enemy])
    Bestiary.enemies[enemy].set_pos(x, y)  # la position de l'enemi est en pourcentage de l'écran
    ratios[Bestiary.enemies[enemy].get_name()] = Bestiary.enemies[enemy].get_width()/scr[0]
    Bestiary.enemies[enemy].load_animations()


def remove_active_enemy(enemy):
    active_enemies.remove(Bestiary.enemies[enemy])


def main():
    global win, scr, active_enemies
    clock = pygame.time.Clock()

    Bestiary.load_enemies()
    add_active_enemy("bad_guy", 75, 40)
    Background.load_backgrounds(scr[0], scr[1])

    p = Player(x=25, y=40, width=125, height=175, max_health=100)  # la position du personnage est en pourcentage de l'écran
    ratios["player_scr_width"] = p.get_width()/scr[0]
    p.load_animations()
    p.get_attributes("status").set_status("poisoned", True, level=1)
    p.get_attributes("status").update_status()

    Background.set_background_active("menu", 10)

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
                if event.size[0]/event.size[1] != ratios["scr"]:
                    new_scr = (int(event.size[0]), int(event.size[0]*720/960))
                else:
                    new_scr = event.size
                p.set_new_size(new_scr, event.size, ratios["player_scr_width"])
                win = pygame.display.set_mode(new_scr, pygame.RESIZABLE)
                scr = win.get_width(), win.get_height()
                Background.resize_active_background(scr[0], scr[1])
                for enemy in active_enemies:
                    enemy.set_new_size(new_scr, event.size, ratios[enemy.get_name()])

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
                    Bestiary.enemies["bad_guy"].set_animation("blinking", Bestiary.enemies["bad_guy"].char, 10, 3)

        redrawGameWindow(win, command, p, active_enemies)


main()

