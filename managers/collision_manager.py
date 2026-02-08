# managers/collision_manager.py
from core.collision_result import CollisionResult
from entities.enemies import AirEnemy


class CollisionManager:
    def check(self, player, enemies):
        for e in enemies[:]:
            # projéteis só matam inimigos aéreos
            if isinstance(e, AirEnemy):
                for p in player.projectiles[:]:
                    if p.rect.colliderect(e.rect):
                        enemies.remove(e)
                        player.projectiles.remove(p)
                        return CollisionResult.AIR_KILLED

            # colisão com player
            if player.rect.colliderect(e.rect):
                return CollisionResult.PLAYER_HIT

        return None
