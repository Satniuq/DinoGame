# systems/input_system.py
import pygame


class InputSystem:
    def __init__(self):
        # -----------------
        # SALTAR
        self.jump_keys = {
            pygame.K_SPACE,
            pygame.K_w,
            pygame.K_KP8,
        }

        # -----------------
        # AGACHAR
        self.crouch_keys = {
            pygame.K_DOWN,
            pygame.K_s,
            pygame.K_KP2,
        }

        # -----------------
        # DISPARAR
        self.shoot_keys = {
            pygame.K_f,
            pygame.K_KP0,
        }

        # -----------------
        # ROLL ESQUERDA
        self.roll_left_keys = {
            pygame.K_a,
            pygame.K_LEFT,
            pygame.K_KP4,
            pygame.K_LSHIFT,
        }

        # -----------------
        # ROLL DIREITA
        self.roll_right_keys = {
            pygame.K_d,
            pygame.K_RIGHT,
            pygame.K_KP6,
            pygame.K_RSHIFT,
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

            # ROLAR PARA A ESQUERDA
            if event.key in self.roll_left_keys:
                world.player.roll(-1)

            # ROLAR PARA A DIREITA
            if event.key in self.roll_right_keys:
                world.player.roll(1)

        elif event.type == pygame.KEYUP:

            # levantar ao largar tecla de agachar
            if event.key in self.crouch_keys:
                world.player.crouch(False)
