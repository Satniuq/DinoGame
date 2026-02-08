# systems/combat_system.py
from core.events import PlayerHit, EnemyKilled, EnemyPassed, PlayerDied

class CombatSystem:
    def __init__(self, bus, player, progress):
        self.bus = bus
        self.player = player
        self.progress = progress

        bus.subscribe(PlayerHit, self.on_player_hit)
        bus.subscribe(EnemyKilled, self.on_enemy_killed)
        bus.subscribe(EnemyPassed, self.on_enemy_passed)

    def on_player_hit(self, event):
        died = self.player.take_damage()
        if died:
            self.bus.emit(PlayerDied())

    def on_enemy_killed(self, event):
        event.enemy.kill()
        self.progress.killed += 1

    def on_enemy_passed(self, event):
        self.progress.passed += 1
