# systems/input_system.py
import pygame

class InputSystem:
    def __init__(self):
        # mapeamento de teclas
        self.jump_keys = {
            pygame.K_SPACE,
            pygame.K_w,
            pygame.K_KP8,
        }

        self.crouch_keys = {
            pygame.K_DOWN,
            pygame.K_s,
            pygame.K_KP2,
        }

        self.shoot_keys = {
            pygame.K_f,
            pygame.K_KP0,
        }

    def handle(self, event, world):
        if event.type == pygame.KEYDOWN:

            # SALTAR
            if event.key in self.jump_keys:
                world.player.jump()

            # DISPARAR
            if event.key in self.shoot_keys:
                world.player.shoot()

            # AGACHAR
            if event.key in self.crouch_keys:
                world.player.crouch(True)

        elif event.type == pygame.KEYUP:

            # levantar ao largar tecla de agachar
            if event.key in self.crouch_keys:
                world.player.crouch(False)

