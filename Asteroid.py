import pygame
import random
import math

screen_width = 1280
screen_height = 768

WHITE = (255, 255, 255)
ORANGE = (169, 90, 0)
GOLD = (255, 215, 0)
ASTEROID_POINTS_1 = [
    (10,0),
    (45,15),
    (80,10),
    (50,80),
    (20,40)
]
ASTEROID_POINTS_2 = [
    (10, 4),
    (38, 5),
    (65, 10),
    (73, 35),
    (63, 65),
    (29, 77),
    (3, 38)
]
ASTEROID_POINTS_3 = [
    (10, 4),
    (38, 5),
    (65, 10),
    (73, 35),
    (70, 44),
    (46, 41),
    (67, 58),
    (63, 65),
    (29, 77),
    (3, 38)
]
POINTS = [ASTEROID_POINTS_1, ASTEROID_POINTS_2, ASTEROID_POINTS_3]
ANGLES = [0, 90, 180, 270]
SPEED = 1


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, position, size, speed=1):
        super().__init__()
        base_size = 80
        final_size = base_size/size
        self.image = pygame.Surface((final_size, final_size), pygame.SRCALPHA)
        points = random.choice(POINTS)
        pygame.draw.polygon(self.image, ORANGE, tuple([x/size, y/size] for (x, y) in points))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        directions = [-1, 0, 1]
        self.vx = speed * random.choice(directions)
        self.vy = speed * random.choice(directions)
        if self.vy == 0 and self.vx == 0:
            self.vy = 1
        self.size = size
        self.position = position
        self.speed = 2
        self.moveNum = 0
        self.image=pygame.transform.rotate(self.image, random.choice(ANGLES))

    def update(self):
        self.moveNum += 1
        if self.moveNum % self.speed == 0:
            self.rect.x += self.vx  # Move horizontally
            self.rect.y += self.vy  # Move vertically
            if self.rect.right < 0:
                self.rect.left = screen_width
            elif self.rect.left > screen_width:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = screen_height
            elif self.rect.top > screen_height:
                self.rect.bottom = 0
    
    def get_size(self):
        return self.size
    
    def get_position(self):
        return (self.rect.x, self.rect.y)

class MoneyPickup(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.sheet = pygame.image.load('1/Coin1.png').convert_alpha()
        sources = [
            pygame.image.load('1/Coin1.png').convert_alpha(),
            pygame.image.load('1/Coin2.png').convert_alpha(),
            pygame.image.load('1/Coin3.png').convert_alpha(),
            pygame.image.load('1/Coin4.png').convert_alpha(),
            pygame.image.load('1/Coin5.png').convert_alpha(),
            pygame.image.load('1/Coin6.png').convert_alpha(),
            pygame.image.load('1/Coin7.png').convert_alpha(),
            pygame.image.load('1/Coin8.png').convert_alpha()
        ]
        self.frames = [
            sources[0].subsurface((20, 20, 25, 25)).copy(),
            sources[1].subsurface((20, 20, 25, 25)).copy(),
            sources[2].subsurface((20, 20, 25, 25)).copy(),
            sources[3].subsurface((20, 20, 25, 25)).copy(),
            sources[4].subsurface((20, 20, 25, 25)).copy(),
            sources[5].subsurface((20, 20, 25, 25)).copy(),
            sources[6].subsurface((20, 20, 25, 25)).copy(),
            sources[7].subsurface((20, 20, 25, 25)).copy()
        ]
        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.life = 0
        self.skip = 0

    def update(self):
        self.life += 1
        if self.life >= 3000:
            self.kill()
        self.skip += 1
        if self.skip%20 == 0:
            self.index += 1
            if self.index == 8:
                self.index = 0
        self.image = self.frames[self.index]