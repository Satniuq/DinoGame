# entities/obstacles.py
import pygame
from settings import *


class Obstacle:
    def __init__(self, rect, speed):
        self.rect = rect
        self.speed = speed
        self.active = True

    def update(self, dt):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (90, 90, 90), self.rect)


class LowObstacle(Obstacle):
    """
    Obstáculo baixo → SALTAR POR CIMA
    """
    def __init__(self, speed):
        rect = pygame.Rect(
            WIDTH + 50,
            GROUND_Y - 30,
            40,
            30
        )
        super().__init__(rect, speed)

    def draw(self, screen):
        pygame.draw.rect(screen, (120, 120, 120), self.rect)


class HighObstacle(Obstacle):
    """
    Obstáculo alto → AGACHAR POR BAIXO
    """
    def __init__(self, speed):
        rect = pygame.Rect(
            WIDTH + 50,
            GROUND_Y - 90,
            40,
            60
        )
        super().__init__(rect, speed)

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 70, 70), self.rect)
