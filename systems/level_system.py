# systems/level_system.py
from core.events import LevelCompleted

class LevelSystem:
    def __init__(self, bus, definition, progress):
        self.bus = bus
        self.definition = definition
        self.progress = progress

    def update(self):
        if self.progress.resolved >= self.definition.total_air_enemies:
            self.bus.emit(LevelCompleted())
