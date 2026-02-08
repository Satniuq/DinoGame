# systems/input_system.py
import pygame

class InputSystem:
    def handle(self, event, world):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.player.jump()
            if event.key == pygame.K_f:
                world.player.shoot()
            if event.key == pygame.K_DOWN:
                world.player.crouch(True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                world.player.crouch(False)
