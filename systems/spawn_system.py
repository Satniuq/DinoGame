# systems/spawn_system.py
import random
import math
from entities.enemies import AirEnemy
from entities.obstacles import LowObstacle, HighObstacle
from entities.boss import BossEnemy


class SpawnSystem:
    def __init__(self, level_def):
        self.level_def = level_def

        self.obstacle_cooldown = 0
        self.last_obstacle_type = None

        self.active_pattern = None
        self.pattern_step = 0
        self.pattern_timer = 0

        # boss
        self.boss_spawned = False

    # ==============================
    # HELPERS
    # ==============================
    def _speed(self) -> float:
        return 4.0 * self.level_def.speed_multiplier

    def _frames_for_gap_px(self, gap_px: float) -> int:
        spd = max(0.001, self._speed())
        return max(1, int(math.ceil(gap_px / spd)))

    def _can_spawn_air(self, progress) -> bool:
        return progress.spawned < self.level_def.total_air_enemies

    def _set_obstacle_cooldown(self, next_type: str):
        base_gap_px = 320
        opposite_gap_px = 480

        if self.last_obstacle_type is None:
            gap = base_gap_px
        elif self.last_obstacle_type != next_type:
            gap = opposite_gap_px
        else:
            gap = base_gap_px

        self.obstacle_cooldown = self._frames_for_gap_px(gap)
        self.last_obstacle_type = next_type

    # ==============================
    # UPDATE
    # ==============================
    def update(self, world, progress):
        # ---------- BOSS LEVEL ----------
        if self.level_def.has_boss:
            if not self.boss_spawned:
                world.enemies.append(BossEnemy(self._speed(), level=self.level_def.level))
                self.boss_spawned = True
            return

        # ---------- PADRÕES ----------
        if self.active_pattern:
            self._update_pattern(world, progress)
            return

        # ---------- INIMIGOS AÉREOS ----------
        if (
            self._can_spawn_air(progress)
            and random.random() < self.level_def.spawn_pressure * 0.02
        ):
            world.enemies.append(AirEnemy(self._speed()))
            progress.spawned += 1

        # ---------- COOLDOWN ----------
        if self.obstacle_cooldown > 0:
            self.obstacle_cooldown -= 1
            return

        # ---------- PADRÕES ----------
        if random.random() < 0.10:
            self._start_pattern()
            return

        # ---------- OBSTÁCULO SIMPLES ----------
        if random.random() < 0.015:
            self._spawn_simple_obstacle(world)

    # ==============================
    # OBSTÁCULOS
    # ==============================
    def _spawn_simple_obstacle(self, world):
        spd = self._speed()

        if self.last_obstacle_type == "low":
            kind = "high"
        elif self.last_obstacle_type == "high":
            kind = "low"
        else:
            kind = random.choice(["low", "high"])

        if kind == "low":
            world.obstacles.append(LowObstacle(spd))
        else:
            world.obstacles.append(HighObstacle(spd))

        self._set_obstacle_cooldown(kind)

    # ==============================
    # PADRÕES
    # ==============================
    def _start_pattern(self):
        self.active_pattern = random.choice([
            "LOW_AIR",
            "HIGH_AIR",
            "LOW_THEN_HIGH",
            "HIGH_THEN_LOW",
        ])
        self.pattern_step = 0
        self.pattern_timer = 0

    def _end_pattern(self):
        self.active_pattern = None
        self.pattern_step = 0
        self.pattern_timer = 0
        self.obstacle_cooldown = self._frames_for_gap_px(280)

    def _update_pattern(self, world, progress):
        self.pattern_timer += 1
        spd = self._speed()

        # --- LOW + AIR ---
        if self.active_pattern == "LOW_AIR":
            if self.pattern_step == 0:
                world.obstacles.append(LowObstacle(spd))
                self.last_obstacle_type = "low"
                self.pattern_step = 1
                self.pattern_timer = 0

            elif self.pattern_timer >= self._frames_for_gap_px(260):
                if self._can_spawn_air(progress):
                    world.enemies.append(AirEnemy(spd))
                    progress.spawned += 1
                self._end_pattern()

        # --- HIGH + AIR ---
        elif self.active_pattern == "HIGH_AIR":
            if self.pattern_step == 0:
                world.obstacles.append(HighObstacle(spd))
                self.last_obstacle_type = "high"
                self.pattern_step = 1
                self.pattern_timer = 0

            elif self.pattern_timer >= self._frames_for_gap_px(260):
                if self._can_spawn_air(progress):
                    world.enemies.append(AirEnemy(spd))
                    progress.spawned += 1
                self._end_pattern()

        # --- LOW -> HIGH ---
        elif self.active_pattern == "LOW_THEN_HIGH":
            if self.pattern_step == 0:
                world.obstacles.append(LowObstacle(spd))
                self.last_obstacle_type = "low"
                self.pattern_step = 1
                self.pattern_timer = 0

            elif self.pattern_timer >= self._frames_for_gap_px(520):
                world.obstacles.append(HighObstacle(spd))
                self._set_obstacle_cooldown("high")
                self._end_pattern()

        # --- HIGH -> LOW ---
        elif self.active_pattern == "HIGH_THEN_LOW":
            if self.pattern_step == 0:
                world.obstacles.append(HighObstacle(spd))
                self.last_obstacle_type = "high"
                self.pattern_step = 1
                self.pattern_timer = 0

            elif self.pattern_timer >= self._frames_for_gap_px(520):
                world.obstacles.append(LowObstacle(spd))
                self._set_obstacle_cooldown("low")
                self._end_pattern()
