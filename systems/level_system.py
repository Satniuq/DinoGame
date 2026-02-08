# systems/level_system.py
from core.events import (
    EnemyKilled,
    EnemyPassed,
    BossDefeated,
    LevelCompleted,
)


class LevelSystem:
    def __init__(self, bus, definition, progress):
        self.bus = bus
        self.definition = definition
        self.progress = progress
        self.completed = False

        bus.subscribe(EnemyKilled, self.on_enemy_killed)
        bus.subscribe(EnemyPassed, self.on_enemy_passed)
        bus.subscribe(BossDefeated, self.on_boss_defeated)

    def on_enemy_killed(self, event):
        if not self.definition.has_boss:
            self.progress.killed += 1

    def on_enemy_passed(self, event):
        if not self.definition.has_boss:
            self.progress.passed += 1

    def on_boss_defeated(self, event):
        if self.completed:
            return
        self.completed = True
        self.bus.emit(LevelCompleted())

    def update(self):
        if self.completed or self.definition.has_boss:
            return

        if self.progress.resolved >= self.definition.total_air_enemies:
            self.completed = True
            self.bus.emit(LevelCompleted())
