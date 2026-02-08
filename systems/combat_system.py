# systems/combat_system.py
from core.events import (
    PlayerHit,
    EnemyKilled,
    BossHit,
    PlayerDied,
    BossDefeated,
)
from entities.boss import BossEnemy


class CombatSystem:
    def __init__(self, bus, player):
        self.bus = bus
        self.player = player

        bus.subscribe(PlayerHit, self.on_player_hit)
        bus.subscribe(EnemyKilled, self.on_enemy_killed)
        bus.subscribe(BossHit, self.on_boss_hit)

    # ======================
    # PLAYER
    # ======================
    def on_player_hit(self, event):
        died = self.player.take_damage()
        if died:
            self.bus.emit(PlayerDied())

    # ======================
    # INIMIGOS NORMAIS
    # ======================
    def on_enemy_killed(self, event):
        enemy = event.enemy
        enemy.kill()

    # ======================
    # BOSS
    # ======================
    def on_boss_hit(self, event):
        boss = event.boss
        boss.take_damage(event.damage)

        if boss.is_dead:
            self.bus.emit(BossDefeated())
