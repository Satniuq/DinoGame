# entities/player.py
import pygame
from settings import *
from entities.projectiles import Projectile


class Player:
    def __init__(self, x=50):
        self.x = x

        # -----------------
        # LIMITES HORIZONTAIS
        self.left_bound = 20
        self.right_bound = WIDTH - 80

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
        self.invul_duration = 60

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
        # ROLL
        self.is_rolling = False
        self.roll_timer = 0
        self.roll_duration = 18
        self.roll_speed = 12
        self.roll_cooldown = 30
        self.roll_cooldown_timer = 0
        self.roll_dir = 1  # +1 direita | -1 esquerda

    # -----------------
    def _update_hitbox(self):
        base_y = self.y + 40

        if self.is_crouching:
            self.rect.width = self.crouch_width
            self.rect.height = self.crouch_height
        else:
            self.rect.width = self.stand_width
            self.rect.height = self.stand_height

        self.rect.bottomleft = (self.x, base_y)

    # -----------------
    def _cancel_roll(self):
        """Cancela o roll e volta ao estado normal (sem mexer na física vertical)."""
        if not self.is_rolling:
            return

        self.is_rolling = False
        self.roll_timer = 0

        # deixa de forçar crouch (se estiver no ar, fica em "stand")
        self.is_crouching = False
        self.crouch_buffer = False

        # não faz sentido manter fast-fall activo ao cancelar com salto
        self.fast_fall = False

    # -----------------
    def update(self, dt):
        # ---------- cooldown roll ----------
        if self.roll_cooldown_timer > 0:
            self.roll_cooldown_timer -= 1

        # ---------- roll ----------
        if self.is_rolling:
            self.roll_timer += 1
            self.x += self.roll_speed * self.roll_dir

            if self.roll_timer >= self.roll_duration:
                self.is_rolling = False
                self.roll_timer = 0
                self.is_crouching = False

        # ---------- física vertical ----------
        self.y += self.vel_y

        if self.fast_fall:
            self.vel_y += GRAVITY * self.fast_fall_multiplier
        else:
            self.vel_y += GRAVITY

        if self.y >= self.y_ground:
            self.y = self.y_ground
            self.vel_y = 0
            self.jump_count = 0
            self.fast_fall = False

            if self.crouch_buffer:
                self.is_crouching = True
                self.crouch_buffer = False

        # ---------- LIMITES HORIZONTAIS ----------
        if self.x < self.left_bound:
            self.x = self.left_bound
        elif self.x > self.right_bound:
            self.x = self.right_bound

        self._update_hitbox()

        # ---------- invulnerabilidade ----------
        if self.invulnerable:
            self.invul_timer += 1
            if self.invul_timer >= self.invul_duration:
                self.invulnerable = False
                self.invul_timer = 0

        # ---------- animação ----------
        self.anim_step = (self.anim_step + 1) % 20

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
        # ✅ CANCEL ROLL: no chão ou no ar enquanto ainda tens salto disponível (jump_count < 2)
        if self.is_rolling:
            on_ground = (self.y >= self.y_ground)
            can_air_cancel = (not on_ground and self.jump_count < 2)

            if on_ground or can_air_cancel:
                self._cancel_roll()
            else:
                return  # não pode cancelar (já gastou double jump)

        # saltar normal (duplo salto incluído)
        if not self.is_crouching and self.jump_count < 2:
            self.vel_y = JUMP_STRENGTH
            self.jump_count += 1

    # -----------------
    def crouch(self, active: bool):
        # enquanto está a rolar, não deixamos o crouch "mexer" no estado
        if self.is_rolling:
            return

        if active:
            if self.y < self.y_ground:
                self.crouch_buffer = True
                self.fast_fall = True
                return

            self.vel_y = 0
            self.jump_count = 0
            self.is_crouching = True
        else:
            self.is_crouching = False
            self.crouch_buffer = False
            self.fast_fall = False

        self._update_hitbox()

    # -----------------
    def roll(self, direction=1):
        if self.roll_cooldown_timer > 0:
            return
        if self.is_rolling:
            return

        self.is_rolling = True
        self.roll_timer = 0
        self.roll_dir = 1 if direction >= 0 else -1
        self.roll_cooldown_timer = self.roll_cooldown

        self.is_crouching = True

        # i-frames durante roll
        self.invulnerable = True
        self.invul_timer = 0
        self.invul_duration = self.roll_duration

    # -----------------
    def shoot(self):
        if not self.is_crouching and len(self.projectiles) < 3:
            self.projectiles.append(
                Projectile(
                    self.rect.right,
                    self.rect.centery,
                    FLAME_SPEED,
                )
            )

    # -----------------
    def reset_lives(self):
        self.lives = self.max_lives
        self.invulnerable = False
        self.invul_timer = 0

    # -----------------
    def draw(self, screen):
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
