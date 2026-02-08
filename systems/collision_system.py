# systems/collision_system.py
from core.events import PlayerHit, EnemyKilled, EnemyPassed

class CollisionSystem:
    def __init__(self, bus):
        self.bus = bus

    def update(self, world):
        # -------- INIMIGOS --------
        for enemy in world.enemies:
            # projécteis ↔ inimigos
            for proj in world.player.projectiles:
                if proj.active and enemy.active and proj.rect.colliderect(enemy.rect):
                    proj.active = False
                    if not enemy.resolved:
                        enemy.resolved = True
                        self.bus.emit(EnemyKilled(enemy))

            # player ↔ inimigos
            if enemy.active and world.player.rect.colliderect(enemy.rect):
                self.bus.emit(PlayerHit())

            # inimigo passou
            if not enemy.active and not enemy.resolved:
                enemy.resolved = True
                self.bus.emit(EnemyPassed(enemy))

        # -------- OBSTÁCULOS --------
        for obs in world.obstacles:
            # chamas NÃO afectam obstáculos → nada aqui
            if obs.active and world.player.rect.colliderect(obs.rect):
                self.bus.emit(PlayerHit())
