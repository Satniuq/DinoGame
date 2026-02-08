import pygame
import random
from settings import *
from entities.base import Entity
from entities.boss_wave import BossWave


class BossEnemy(Entity):
    def __init__(self, speed, level=5):
        rect = pygame.Rect(
            WIDTH + 120,
            GROUND_Y - 140,
            160,
            120,
        )
        super().__init__(rect, speed)

        # -----------------
        # ESCALA COM O NÍVEL
        # -----------------
        self.level = level
        self.max_hp = 8 + level * 2
        self.hp = self.max_hp

        self.attack_cooldown = max(40, 100 - level * 5)
        self.wave_speed = 3 + level * 0.4

        # -----------------
        # ESTADO
        # -----------------
        self.state = "ENTER"
        self.timer = 0
        self.attack_timer = 0
        self.is_dead = False

        # -----------------
        # MOVIMENTO
        # -----------------
        self.target_x = WIDTH - 260
        self.vel_y = 0
        self.on_ground = True

        # -----------------
        # FLAGS
        # -----------------
        self.active = True
        self.resolved = False

    # =========================
    def update(self, dt, world=None):
        if self.is_dead:
            self.active = False
            return

        if self.state == "ENTER":
            self._enter()

        elif self.state == "IDLE":
            self._idle()

        elif self.state == "ATTACK_GROUND":
            self._attack_ground(world)

        elif self.state == "ATTACK_AIR":
            self._attack_air(world)

        elif self.state == "JUMP_ATTACK":
            self._jump_attack(world)

        self._apply_gravity()

    # =========================
    def _enter(self):
        self.rect.x -= self.speed
        if self.rect.x <= self.target_x:
            self.rect.x = self.target_x
            self.state = "IDLE"
            self.timer = 0

    def _idle(self):
        self.timer += 1
        if self.timer >= self.attack_cooldown:
            self.timer = 0
            self._choose_attack()

    # =========================
    def _choose_attack(self):
        self.state = random.choice([
            "ATTACK_GROUND",
            "ATTACK_AIR",
            "JUMP_ATTACK",
        ])
        self.attack_timer = 0

        if self.state == "JUMP_ATTACK":
            self.vel_y = -12
            self.on_ground = False

    # =========================
    def _attack_ground(self, world):
        self.attack_timer += 1
        if self.attack_timer == 10:
            world.obstacles.append(
                BossWave(
                    self.rect.left,
                    GROUND_Y - 30,
                    self.wave_speed,
                    30,
                )
            )

        if self.attack_timer > 30:
            self.state = "IDLE"

    # =========================
    def _attack_air(self, world):
        self.attack_timer += 1
        if self.attack_timer == 10:
            world.obstacles.append(
                BossWave(
                    self.rect.left,
                    GROUND_Y - 90,
                    self.wave_speed,
                    60,
                )
            )

        if self.attack_timer > 30:
            self.state = "IDLE"

    # =========================
    def _jump_attack(self, world):
        self.attack_timer += 1

        if self.attack_timer in (15, 30):
            world.obstacles.append(
                BossWave(
                    self.rect.left,
                    self.rect.bottom - 40,
                    self.wave_speed,
                    40,
                )
            )

        if self.on_ground and self.attack_timer > 40:
            self.state = "IDLE"

    # =========================
    def _apply_gravity(self):
        if not self.on_ground:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
                self.vel_y = 0
                self.on_ground = True

    # =========================
    def take_damage(self, amount=1):
        if self.is_dead:
            return

        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True

    # =========================
    def draw(self, screen):
        if self.is_dead:
            return

        pygame.draw.rect(screen, (120, 20, 20), self.rect)

        # HP bar
        ratio = self.hp / self.max_hp
        bar_w = 160
        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (self.rect.x, self.rect.y - 15, bar_w, 8),
        )
        pygame.draw.rect(
            screen,
            (200, 40, 40),
            (self.rect.x, self.rect.y - 15, int(bar_w * ratio), 8),
        )
