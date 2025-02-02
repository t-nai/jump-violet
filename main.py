import pygame
import random
import sys
from pygame.locals import *


class Girl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("girl.png")
        self.image = pygame.transform.scale(self.image, (25, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (70, 300)
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed


class Pillar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.poster_y = self.spawn()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        self.mask = pygame.mask.from_surface(self.image)

    def spawn(self):
        images = [['pillars1.png', 200], ['pillars2.png', 100], ['pillars3.png', 400], ['pillars4.png', 400]]
        i = random.randrange(4)
        self.image = pygame.image.load(images[i][0]).convert_alpha()
        self.rect = self.image.get_rect()
        return images[i][1]

    def get_poster_y(self):
        return self.poster_y


class Poster(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        size_x = 170
        size_y = 130
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed


class Button:
    def __init__(self, x, y, l, h, fill, text):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.fill = fill
        self.text = text
        self.font = pygame.font.SysFont("VT323", 45)

    def create(self, screen):
        pygame.draw.rect(screen, self.fill, (self.x, self.y, self.l, self.h))
        text_render = self.font.render(self.text, False, (255, 255, 255))
        text_pos = text_render.get_rect(center=(self.x + self.l // 2, self.y + self.h // 2))
        screen.blit(text_render, text_pos)

    def clicked(self, mouse_pos):
        x, y = mouse_pos
        return self.x <= x <= self.x + self.l and self.y <= y <= self.y + self.h


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    background = pygame.image.load('background.png').convert()
    background = pygame.transform.scale(background, (800, 600))
    pygame.display.set_caption("Jump, Violet!")
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)

    start_button = Button(300, 260, 200, 50, (48, 25, 52), "START")
    restart_button = Button(300, 260, 200, 50, (48, 25, 52), "PLAY AGAIN")

    clock = pygame.time.Clock()

    game = False
    restart = False
    girl = None
    pillars = None
    posters = None
    all_sprites = None

    def reset():
        nonlocal girl, all_sprites, pillars, posters, game, restart

        girl = Girl()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(girl)
        pillars = pygame.sprite.Group()
        posters = pygame.sprite.Group()

        for i in range(10):
            coor_x = 500 + (i * 500)
            pillar = Pillar(coor_x, 0)
            poster = Poster((coor_x + 60), pillar.get_poster_y(), which_image(i))
            all_sprites.add(pillar, poster)
            pillars.add(pillar)
            posters.add(poster)

        game = True
        restart = False

    def which_image(index):
        return ["1759 1.png", "1842 1.png", "1875 1.png", "1940s 1.png", "1942 1.png", "1950s 1.png", "1952 1.png",
                "1960 1.png", "1961 1.png", "2000s 1.png"][index]


    def collision(girl, pillar):
        offset = (pillar.rect.x - girl.rect.x, pillar.rect.y - girl.rect.y)
        return girl.mask.overlap(pillar.mask, offset)


    while True:
        screen.blit(background, (0, 0))

        if not game:
            start_button.create(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game == False and start_button.clicked(event.pos):
                    game = True
                    reset()
                elif restart and restart_button.clicked(event.pos):
                    reset()

        if game == True:
            all_sprites.update()
            all_sprites.draw(screen)

            for pillar in pillars:
                if collision(girl, pillar) != None:
                    game = False
                    restart = True
                    break

            if girl.rect.top <= 0 or girl.rect.bottom >= 600:
                game = False
                restart = True

            if all(pillar.rect.right < 0 for pillar in pillars):
                restart = True

        if restart:
            restart_button.create(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
