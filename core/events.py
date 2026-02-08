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

class LevelWon(Event):
    pass

class LevelFailed(Event):
    pass

class BossDefeated(Event):
    pass

class BossHit:
    def __init__(self, boss, damage=1):
        self.boss = boss
        self.damage = damage

