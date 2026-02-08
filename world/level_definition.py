# world/level_definition.py

class LevelDefinition:
    def __init__(self, level=1):
        self.level = level
        self.total_air_enemies = 20 + (level - 1) * 5
        self.min_kill_ratio = max(0.4, 0.6 - level * 0.02)

        self.speed_multiplier = 1.0 + (level - 1) * 0.15
        self.spawn_pressure = min(1.0, 0.6 + level * 0.05)
