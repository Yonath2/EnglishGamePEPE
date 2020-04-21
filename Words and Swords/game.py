import pygame
from player import Player
from bestiary import Bestiary
from background import Background
from words_and_synonyms import Words

pygame.init()

scr = [700, 700]

win = pygame.display.set_mode(scr, pygame.RESIZABLE)
pygame.display.set_caption("Words and Swords")


def redrawGameWindow(win, command, player, enemies):
    font = pygame.font.SysFont("times new roman", 40, 10)

    win.fill((255,255,255))

    Background.display_background(win)

    player.draw(win)
    player.play_animation()
    for enemy in enemies:
        enemy.draw(win)

    text = font.render(command, 1, (255, 255, 255), (0, 0, 0))
    win.blit(text, (scr[0]/2 - text.get_width()/2, scr[1] - text.get_height()))

    pygame.display.flip()


def main():
    global win, scr
    clock = pygame.time.Clock()

    Bestiary.load_enemies()
    Background.load_backgrounds()

    p = Player(50, 50, 50, 100, 100)
    p.get_attributes("status").set_status("poisoned", True, level=1)
    p.get_attributes("status").update_status()

    Background.set_background_active("menu")

    active_enemies = []
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

            if event.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                scr = win.get_width(), win.get_height()
                Background.resize_backgrounds(scr[0], scr[1])

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

        redrawGameWindow(win, command, p, active_enemies)


main()

