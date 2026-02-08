# entities/base.py
import pygame

class Entity:
    def __init__(self, rect: pygame.Rect, speed: int = 0):
        self.rect = rect
        self.speed = speed
        self.active = True

    def update(self, dt):
        pass

    def draw(self, screen):
        raise NotImplementedError
