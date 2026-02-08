# settings.py
import pygame  # (podes nem usar aqui, mas não faz mal)

WIDTH, HEIGHT = 900, 400
FPS = 60

# Cores
WHITE = (247, 247, 247)
BLACK = (32, 33, 36)
RED = (200, 50, 50)
GREEN = (34, 177, 76)
ORANGE = (255, 140, 0)
GRAY = (100, 100, 100)

# Física e Gameplay
GRAVITY = 0.6
JUMP_STRENGTH = -12
FLAME_SPEED = 25

BASE_SPEED = 6
GROUND_Y = 350  # linha do chão (visual)
DINO_GROUND_Y = 310  # y do corpo do dino (como tinhas)
