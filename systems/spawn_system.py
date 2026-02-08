# systems/spawn_system.py
import random
import math
from entities.enemies import AirEnemy
from entities.obstacles import LowObstacle, HighObstacle

class SpawnSystem:
    def __init__(self, level_def):
        self.level_def = level_def

        # --------- CONTROLO DE SPAWN ---------
        self.obstacle_cooldown = 0          # em frames (calculado a partir de px/velocidade)
        self.last_obstacle_type = None      # "low" / "high"

        # padrões
        self.active_pattern = None
        self.pattern_step = 0
        self.pattern_timer = 0

    # ==============================
    # Helpers: gap em pixels -> frames
    # ==============================
    def _speed(self) -> float:
        # garante consistência com o que já usas
        return 4.0 * self.level_def.speed_multiplier

    def _frames_for_gap_px(self, gap_px: float) -> int:
        # frames ≈ distância / velocidade
        spd = max(0.001, self._speed())
        return max(1, int(math.ceil(gap_px / spd)))

    def _set_obstacle_cooldown(self, next_type: str):
        """
        Define o cooldown com base no tipo a seguir e no último tipo.
        Regras:
        - gap base para obstáculos "normais"
        - gap maior quando a acção é oposta (low <-> high)
        """
        # Ajusta estes valores para dificuldade:
        base_gap_px = 320   # espaço mínimo "normal"
        opposite_gap_px = 480  # espaço mínimo quando é LOW -> HIGH ou HIGH -> LOW

        if self.last_obstacle_type is None:
            gap = base_gap_px
        elif self.last_obstacle_type != next_type:
            gap = opposite_gap_px
        else:
            gap = base_gap_px

        self.obstacle_cooldown = self._frames_for_gap_px(gap)
        self.last_obstacle_type = next_type

    # ==============================
    # Update
    # ==============================
    def update(self, world, progress):
        # 1) Se um padrão estiver activo, continua-o e não faz mais nada
        if self.active_pattern:
            self._update_pattern(world, progress)
            return

        # 2) Spawn normal de inimigos aéreos (conta para o nível)
        if (
            progress.spawned < self.level_def.total_air_enemies
            and random.random() < self.level_def.spawn_pressure * 0.02
        ):
            enemy = AirEnemy(self._speed())
            world.enemies.append(enemy)
            progress.spawned += 1

        # 3) Cooldown de obstáculos
        if self.obstacle_cooldown > 0:
            self.obstacle_cooldown -= 1
            return

        # 4) Chance de começar um padrão (quando não há cooldown)
        # (se quiseres menos padrões, baixa este valor)
        if random.random() < 0.10:
            self._start_pattern()
            return

        # 5) Obstáculo simples
        if random.random() < 0.015:
            self._spawn_simple_obstacle(world)

    # ==============================
    # Obstáculos simples
    # ==============================
    def _spawn_simple_obstacle(self, world):
        spd = self._speed()

        # para evitar repetir o mesmo tipo sempre:
        # (mas ainda permite se quiseres — aqui evitamos repetições seguidas)
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
    # Padrões combinados
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
        # no fim do padrão, força algum espaço antes de voltar ao “normal”
        # (usa base_gap para não levar logo outro obstáculo em cima)
        self.obstacle_cooldown = self._frames_for_gap_px(280)

    def _update_pattern(self, world, progress):
        self.pattern_timer += 1
        spd = self._speed()

        # --- LOW + AIR (salto + tiro) ---
        if self.active_pattern == "LOW_AIR":
            if self.pattern_step == 0:
                world.obstacles.append(LowObstacle(spd))
                self.pattern_step = 1
                self.pattern_timer = 0
                # aqui tratamos como se o último obstáculo fosse low
                self.last_obstacle_type = "low"

            elif self.pattern_step == 1:
                # inimigo vem após uma distância razoável (em px)
                if self.pattern_timer >= self._frames_for_gap_px(260):
                    if progress.spawned < self.level_def.total_air_enemies:
                        world.enemies.append(AirEnemy(spd))
                        progress.spawned += 1
                    self._end_pattern()

        # --- HIGH + AIR (agachar + tiro) ---
        elif self.active_pattern == "HIGH_AIR":
            if self.pattern_step == 0:
                world.obstacles.append(HighObstacle(spd))
                self.pattern_step = 1
                self.pattern_timer = 0
                self.last_obstacle_type = "high"

            elif self.pattern_step == 1:
                if self.pattern_timer >= self._frames_for_gap_px(260):
                    if progress.spawned < self.level_def.total_air_enemies:
                        world.enemies.append(AirEnemy(spd))
                        progress.spawned += 1
                    self._end_pattern()

        # --- LOW -> HIGH (salto -> agachar) ---
        elif self.active_pattern == "LOW_THEN_HIGH":
            if self.pattern_step == 0:
                world.obstacles.append(LowObstacle(spd))
                self.pattern_step = 1
                self.pattern_timer = 0
                self.last_obstacle_type = "low"

            elif self.pattern_step == 1:
                # gap MAIOR porque é acção oposta
                if self.pattern_timer >= self._frames_for_gap_px(520):
                    world.obstacles.append(HighObstacle(spd))
                    # actualizar cooldown como oposto
                    self._set_obstacle_cooldown("high")
                    self._end_pattern()

        # --- HIGH -> LOW (agachar -> salto) ---
        elif self.active_pattern == "HIGH_THEN_LOW":
            if self.pattern_step == 0:
                world.obstacles.append(HighObstacle(spd))
                self.pattern_step = 1
                self.pattern_timer = 0
                self.last_obstacle_type = "high"

            elif self.pattern_step == 1:
                if self.pattern_timer >= self._frames_for_gap_px(520):
                    world.obstacles.append(LowObstacle(spd))
                    self._set_obstacle_cooldown("low")
                    self._end_pattern()
