# managers/spawn_manager.py
from entities.enemies import AirEnemy
from entities.obstacles import LowObstacle, HighObstacle
from settings import *
import random


class SpawnManager:
    def __init__(self, level_manager):
        self.level = level_manager

        # =====================================================
        # PROGRESSÃO (derivada do LevelManager)
        # =====================================================
        self.speed = BASE_SPEED * self.level.speed_multiplier

        # inimigos aparecem mais rápido com o nível
        self.spawn_delay = max(
            20,
            int(45 / self.level.spawn_pressure),
        )

        # =====================================================
        # TIMERS
        # =====================================================
        self.spawn_timer = 0
        self.obstacle_timer = 0

        # =====================================================
        # OBSTÁCULOS — burst + cooldown (escalável)
        # =====================================================
        self.min_gap = max(25, 50 - self.level.level * 2)
        self.max_gap = max(60, 120 - self.level.level * 5)

        self.current_burst = 0
        self.max_burst = min(5, 2 + self.level.level // 2)

        self.obstacle_cooldown = random.randint(
            self.min_gap,
            self.max_gap,
        )

        self.max_obstacles = 5

    # =====================================================
    def update(self):
        # não spawnar se o nível acabou
        if self.level.is_finished():
            return

        # -----------------
        # INIMIGOS AÉREOS (objetivo do nível)
        # -----------------
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            if self.level.spawned_air < self.level.total_air_enemies:
                self.level.enemies.append(
                    AirEnemy(self.speed)
                )
                self.level.spawned_air += 1

            self.spawn_timer = 0

        # -----------------
        # OBSTÁCULOS (pressão contínua)
        # -----------------
        self.obstacle_timer += 1

        # dentro de um burst
        if self.current_burst > 0:
            if self.obstacle_timer >= self.min_gap:
                if self.count_obstacles() < self.max_obstacles:
                    self.level.enemies.append(
                        self.random_obstacle()
                    )

                self.current_burst -= 1
                self.obstacle_timer = 0

                # terminou burst → novo cooldown
                if self.current_burst == 0:
                    self.obstacle_cooldown = random.randint(
                        self.min_gap,
                        self.max_gap,
                    )

        # fora de burst → esperar cooldown
        else:
            if self.obstacle_timer >= self.obstacle_cooldown:
                self.current_burst = random.randint(
                    1,
                    self.max_burst,
                )
                self.obstacle_timer = 0

    # =====================================================
    def random_obstacle(self):
        """
        Escolha do tipo de obstáculo.
        Com o nível, aparecem mais obstáculos altos.
        """
        # probabilidade de obstáculo baixo diminui com o nível
        chance_low = max(
            0.3,
            0.7 - self.level.level * 0.05,
        )

        if random.random() < chance_low:
            return LowObstacle(self.speed)
        return HighObstacle(self.speed)

    # =====================================================
    def count_obstacles(self):
        from entities.obstacles import LowObstacle, HighObstacle
        return sum(
            isinstance(e, (LowObstacle, HighObstacle))
            for e in self.level.enemies
        )
