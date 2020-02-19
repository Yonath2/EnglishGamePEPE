import pygame, math as m, random

pygame.init()

scr = 700,700

win = pygame.display.set_mode(scr)

pygame.display.set_caption('English game')


class Player:
    def __init__(self, x, y, w, h, health):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = (self.x, self.y, self.w, self.h)
        self.synonyms = []
        self.words = ["attack", "block", "heal"]
        self.stat = [10, 5, 20]
        self.font = pygame.font.SysFont("gabriola", 30)
        self.health = health
        self.armor = 0

    def word_and_synonym(self, category):
        words = []
        categories = []
        self.synonyms = []
        with open("Words.txt", "r") as f:
            file = f.readlines()
            for index, string in enumerate(file):
                file[index] = string.replace('\n', '')
            for string in file:
                if string[0] == "#":
                    categories.append(string)
            if category == "noun":
                for i in range(file.index(categories[0])+1, file.index(categories[1])):
                    words.append(file[i])
            if category == "verb":
                for i in range(file.index(categories[1])+1, file.index(categories[2])):
                    words.append(file[i])
            if category == "adjective":
                for i in range(file.index(categories[2])+1, len(file)):
                    words.append(file[i])
            #word = random.choice(words)
            word = "time"
            synonyms = []
            with open("Synonyms.txt") as f:
                file = f.readlines()
                for index, string in enumerate(file):
                    file[index] = string.replace('\n', '')
                for i in range(file.index("#" + word) + 1, len(file)):
                    if file[i][0] == "#":
                        break
                    else:
                        synonyms.append(file[i])
            for synonym in synonyms:
                self.synonyms.append([synonym, False])
            self.synonyms.append(word)

    def effect(self, command, bonus, target=None):
        bonus *= 2
        if command == "attack":
            target.health -= self.stat[self.words.index(command)] + bonus
            return command
        elif command == "block":
            self.armor += self.stat[self.words.index(command)] + bonus
            return command
        elif command == "heal":
            self.health += (self.stat[self.words.index(command)] + bonus) if self.health + self.stat[self.words.index(command)] < 100 else 100 - self.health
            return command

    def draw(self, win, time, status):
        self.rect = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(win, (0,255,255), self.rect)
        angle = m.radians(360/len(self.words))
        if status == "command":
            for index, word in enumerate(self.words, 1):
                WORD = self.font.render(word, 1, (0,100,0))
                x, y = m.cos(index * angle + m.radians(time % 360)) * (self.w + 30) ,  m.sin(index * angle + m.radians(time % 360)) * (self.w + 30)
                win.blit(WORD, (self.x + self.w / 2 + x - WORD.get_width()/2, self.y + self.h / 2 + y- WORD.get_height()/2))
        elif status == "action":
            angle = m.radians(360/(len(self.synonyms)-1))
            for index, word in enumerate(self.synonyms[:-1], 1):
                if word[1]:
                    WORDS = self.font.render(word[0], 1, (0, 200, 0))
                    x, y = m.cos(index * angle + m.radians(time % 360)) * (self.w + 30), m.sin(index * angle + m.radians(time % 360)) * (self.w + 30)
                    win.blit(WORDS, (self.x + self.w / 2 + x - WORDS.get_width()/2, self.y + self.h / 2 + y - WORDS.get_height()))
            WORD = self.font.render("The word is: " + self.synonyms[-1], 1, (0,200,0))
            win.blit(WORD, (20, scr[1] - 50 - WORD.get_height()))
        ARMOR = self.font.render(str(self.armor), 1, (100, 100, 100))
        win.blit(ARMOR, (self.x + self.w/2 - ARMOR.get_width()/2, self.y + self.h/2 - ARMOR.get_height()/2))
        pygame.draw.rect(win, (255,0,0), (self.x + 50 - self.w, self.y + 150, 100, 20))
        pygame.draw.rect(win, (0,255,0), (self.x + 50 - self.w, self.y + 150, self.health, 20))


class Enemy:
    def __init__(self, x, y, w, h, health):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = (self.x, self.y, self.w, self.h)
        self.health = health

    def draw(self, win):
        self.rect = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(win, (255,100,100), self.rect)
        pygame.draw.rect(win, (255,0,0), (self.x + 75 - self.w, self.y + 150, 50, 20))
        pygame.draw.rect(win, (0,255,0), (self.x + 75 - self.w, self.y + 150, self.health, 20))


class Timer:
    def __init__(self):
        self.last = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('gabriola', 40)
        self.now = 0

    def timer(self, milliseconds):
        now = pygame.time.get_ticks()
        if now - self.last >= milliseconds:
            return True
        else:
            self.now = int((milliseconds - (now - self.last))/1000)

    def draw(self, win):
        TIME = self.font.render(f'You got {self.now} seconds left!', 1, (255,255,255))
        win.blit(TIME, (10, 0))


def main():
    fps = 60
    pygame.time.Clock().tick(fps)
    font = pygame.font.SysFont("gabriola", 30)

    def redrawGameWindow():
        win.fill((0,0,0))
        player.draw(win, time, status)
        enemy.draw(win)
        if active:
            pygame.draw.rect(win, (255,255,255), input_box, 5)
        else:
            pygame.draw.rect(win, (128,128,128), input_box, 5)
        pygame.draw.rect(win, (0,0,0), input_box)
        win.blit(font.render(command, 1, (255,255,255)), (20, scr[1] - 50))
        if action_phase:
            clock.draw(win)
        pygame.display.flip()

    player = Player(scr[0]/5, scr[1]*(10/20), 64, 64, 100)
    enemy = Enemy(scr[0] * 4 / 5, scr[1] * (10 / 20), 64, 64, 50)
    time = 0
    active = False
    command_phase = True
    action_phase = False
    enemy_phase = False
    clock = Timer()
    status = "command"
    command = 'input'
    input_box = pygame.Rect((20, scr[1] - 50, scr[0]-40, 30))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if event.button == 1:
                    if input_box.collidepoint(mouse_x, mouse_y):
                        active = True
                        if command == 'input':
                            command = ''
                    else:
                        active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if command_phase:
                            for word in player.words:
                                if command.lower() == word:
                                    if command == "attack":
                                        player.word_and_synonym("noun")
                                    elif command == "block":
                                        player.word_and_synonym("verb")
                                    elif command == "attack":
                                        player.word_and_synonym("adjective")
                                    command = ''
                                    command_phase = False
                                    action_phase = True
                                    status = "action"
                                    clock.last = pygame.time.get_ticks()
                        if action_phase:
                            for synonym in player.synonyms[:-1]:
                                if command == synonym[0]:
                                    synonym[1] = True
                                    command = ''

                    elif event.key == pygame.K_ESCAPE:
                        active = False

                    elif event.key == pygame.K_BACKSPACE:
                        command = command[:-1]
                    else:
                        command += event.unicode

        if action_phase:
            if clock.timer(20_000):
                bonus = sum([0+1 for index, i in enumerate(player.synonyms) if i[1]])
                player.effect("attack", bonus, enemy)
                action_phase = False
                command_phase = True
                status = "command"

        time += 1/fps
        redrawGameWindow()


if __name__ == '__main__':
    main(), pygame.quit()
