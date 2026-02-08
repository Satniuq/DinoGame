import pygame
from settings import *
from entities.projectiles import Projectile


class Player:
    def __init__(self, x=50):
        self.x = x

        # -----------------
        # posição base
        self.y_ground = DINO_GROUND_Y
        self.y = self.y_ground

        # -----------------
        # VIDAS
        self.max_lives = 3
        self.lives = self.max_lives

        self.invulnerable = False
        self.invul_timer = 0
        self.invul_duration = 60  # frames (~1s)

        # -----------------
        # estados
        self.is_crouching = False

        # buffer / fast-fall
        self.crouch_buffer = False
        self.fast_fall = False
        self.fast_fall_multiplier = 2.5

        # -----------------
        # física
        self.vel_y = 0
        self.jump_count = 0

        # -----------------
        # hitbox
        self.stand_width = 45
        self.stand_height = 60
        self.crouch_width = 45
        self.crouch_height = 25

        self.rect = pygame.Rect(self.x, 0, self.stand_width, self.stand_height)
        self._update_hitbox()

        # -----------------
        self.projectiles = []
        self.anim_step = 0

    # -----------------
    def _update_hitbox(self):
        base_y = self.y + 40  # corpo + pernas

        if self.is_crouching:
            self.rect.width = self.crouch_width
            self.rect.height = self.crouch_height
        else:
            self.rect.width = self.stand_width
            self.rect.height = self.stand_height

        self.rect.bottomleft = (self.x, base_y)

    # -----------------
    def update(self):
        # ---------- física ----------
        self.y += self.vel_y

        if self.fast_fall:
            self.vel_y += GRAVITY * self.fast_fall_multiplier
        else:
            self.vel_y += GRAVITY

        # tocar no chão
        if self.y >= self.y_ground:
            self.y = self.y_ground
            self.vel_y = 0
            self.jump_count = 0
            self.fast_fall = False

            # aplicar buffer de agachar
            if self.crouch_buffer:
                self.is_crouching = True
                self.crouch_buffer = False

        self._update_hitbox()

        # ---------- invulnerabilidade ----------
        if self.invulnerable:
            self.invul_timer += 1
            if self.invul_timer >= self.invul_duration:
                self.invulnerable = False
                self.invul_timer = 0

        # ---------- animação ----------
        self.anim_step = (self.anim_step + 1) % 20

        # ---------- projécteis ----------
        for p in self.projectiles[:]:
            p.update()
            if not p.active:
                self.projectiles.remove(p)

    # -----------------
    def take_damage(self):
        if self.invulnerable:
            return False

        self.lives -= 1
        self.invulnerable = True
        self.invul_timer = 0
        return self.lives <= 0

    # -----------------
    def jump(self):
        if not self.is_crouching and self.jump_count < 2:
            self.vel_y = JUMP_STRENGTH
            self.jump_count += 1

    # -----------------
    def crouch(self, active: bool):
        if active:
            # se estiver no ar → buffer + fast fall
            if self.y < self.y_ground:
                self.crouch_buffer = True
                self.fast_fall = True
                return

            # no chão → agacha imediatamente
            self.vel_y = 0
            self.jump_count = 0
            self.is_crouching = True

        else:
            self.is_crouching = False
            self.crouch_buffer = False
            self.fast_fall = False

        self._update_hitbox()

    # -----------------
    def shoot(self):
        if not self.is_crouching and len(self.projectiles) < 3:
            self.projectiles.append(
                Projectile(self.rect.right, self.rect.centery, FLAME_SPEED)
            )

    # -----------------
    def reset_lives(self):
        self.lives = self.max_lives
        self.invulnerable = False
        self.invul_timer = 0

    # -----------------
    def draw(self, screen):
        # pisca quando invulnerável
        if self.invulnerable and self.invul_timer % 10 < 5:
            return

        color = BLACK if not self.is_crouching else (60, 60, 60)

        if self.is_crouching:
            pygame.draw.rect(screen, color, self.rect)
        else:
            pygame.draw.rect(screen, color, (self.x, self.y, 40, 30))
            pygame.draw.rect(screen, color, (self.x + 20, self.y - 20, 25, 25))

            leg_y = self.y + 30
            if self.anim_step < 10:
                pygame.draw.rect(screen, color, (self.x + 5, leg_y, 10, 10))
            else:
                pygame.draw.rect(screen, color, (self.x + 25, leg_y, 10, 10))

        for p in self.projectiles:
            p.draw(screen)
