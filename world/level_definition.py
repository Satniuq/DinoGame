# world/level_definition.py
from settings import (
    GAME_PROFILE,
    DEV_EARLY_LEVEL_ENEMIES,
    DEV_LATE_LEVEL_ENEMIES,
    DEV_MIN_KILL_RATIO,
)


class LevelDefinition:
    def __init__(self, level: int):
        self.level = level

        # -----------------
        # BOSS
        # -----------------
        self.has_boss = (level % 5 == 0)

        # -----------------
        # INIMIGOS DO NÍVEL
        # -----------------
        if GAME_PROFILE == "DEV":
            if level < 5:
                self.total_air_enemies = DEV_EARLY_LEVEL_ENEMIES
            else:
                self.total_air_enemies = DEV_LATE_LEVEL_ENEMIES
        else:
            self.total_air_enemies = 20 + (level - 1) * 5

        # -----------------
        # CONDIÇÃO DE VITÓRIA
        # -----------------
        if GAME_PROFILE == "DEV":
            self.min_kill_ratio = DEV_MIN_KILL_RATIO
        else:
            self.min_kill_ratio = max(0.4, 0.6 - level * 0.02)

        # -----------------
        # DIFICULDADE
        # -----------------
        self.speed_multiplier = 1.0 + (level - 1) * 0.15
        self.spawn_pressure = min(1.0, 0.6 + level * 0.05)
