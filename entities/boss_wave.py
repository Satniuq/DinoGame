import pygame
from settings import WIDTH, GROUND_Y, RED


class BossWave:
    def __init__(self, x, y, speed, height):
        self.rect = pygame.Rect(x, y, 60, height)
        self.speed = speed
        self.active = True

    def update(self, dt):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 50, 50), self.rect)
