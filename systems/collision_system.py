# systems/collision_system.py
from core.events import (
    PlayerHit,
    EnemyKilled,
    EnemyPassed,
    BossHit,
)
from entities.boss import BossEnemy


class CollisionSystem:
    def __init__(self, bus):
        self.bus = bus

    def update(self, world):
        player_hit = False  # evita múltiplos hits no mesmo frame

        # ======================
        # INIMIGOS / BOSS
        # ======================
        for enemy in world.enemies:

            # -------- projécteis do jogador ↔ inimigos --------
            for proj in world.player.projectiles:
                if (
                    proj.active
                    and enemy.active
                    and proj.rect.colliderect(enemy.rect)
                ):
                    proj.active = False

                    # --- BOSS ---
                    if isinstance(enemy, BossEnemy):
                        self.bus.emit(BossHit(enemy, damage=1))

                    # --- INIMIGO NORMAL ---
                    else:
                        if not enemy.resolved:
                            enemy.resolved = True
                            self.bus.emit(EnemyKilled(enemy))

            # -------- player ↔ inimigos --------
            if enemy.active and world.player.rect.colliderect(enemy.rect):
                if not player_hit:
                    self.bus.emit(PlayerHit())
                    player_hit = True

            # -------- inimigo passou --------
            if not enemy.active and not enemy.resolved:
                enemy.resolved = True
                self.bus.emit(EnemyPassed(enemy))

        # ======================
        # OBSTÁCULOS
        # ======================
        for obs in world.obstacles:
            if obs.active and world.player.rect.colliderect(obs.rect):
                if not player_hit:
                    self.bus.emit(PlayerHit())
                    player_hit = True
