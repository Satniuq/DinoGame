# entities/projectiles.py
import pygame
from settings import *

class Projectile:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 25, 15)
        self.speed = speed
        self.active = True

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.active = False

    def draw(self, screen):
        pygame.draw.ellipse(screen, ORANGE, self.rect)
        pygame.draw.ellipse(
            screen,
            (255, 255, 0),
            (self.rect.x + 5, self.rect.y + 3, 15, 8),
        )
