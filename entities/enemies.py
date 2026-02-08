# entities/enemies.py
import pygame
import random
from settings import *
from entities.base import Entity

class Enemy(Entity):
    def __init__(self, rect, speed):
        super().__init__(rect, speed)
        self.active = True
        self.resolved = False   # 👈 MUITO IMPORTANTE

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.active = False

    def kill(self):
        self.active = False


class AirEnemy(Enemy):
    def __init__(self, speed):
        rect = pygame.Rect(
            WIDTH + 50,
            random.choice([
                GROUND_Y - 160,
                GROUND_Y - 200,
            ]),
            40,
            25,
        )
        super().__init__(rect, speed)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)


class GroundEnemy(Enemy):
    def __init__(self, speed):
        rect = pygame.Rect(
            WIDTH + 50,
            GROUND_Y - 30,
            30,
            30
        )
        super().__init__(rect, speed)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 50, 200), self.rect)
