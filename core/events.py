# core/events.py

class Event:
    pass


class PlayerHit(Event):
    pass


class PlayerDied(Event):
    pass


class EnemyKilled(Event):
    def __init__(self, enemy):
        self.enemy = enemy


class EnemyPassed(Event):
    def __init__(self, enemy):
        self.enemy = enemy


class LevelCompleted(Event):
    pass
