# world/level_progress.py

class LevelProgress:
    def __init__(self):
        self.spawned = 0
        self.killed = 0
        self.passed = 0
    
    def enemy_killed(self):
        self.killed += 1

    def enemy_passed(self):
        self.passed += 1

    @property
    def resolved(self):
        return self.killed + self.passed
