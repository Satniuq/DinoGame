# systems/lifetime_system.py

class LifetimeSystem:
    def update(self, world):
        # remove inimigos inactivos
        world.enemies[:] = [e for e in world.enemies if e.active]

        # remove obstáculos inactivos
        world.obstacles[:] = [o for o in world.obstacles if o.active]

        # remove projécteis inactivos (IMPORTANTE: estão no player)
        world.player.projectiles[:] = [p for p in world.player.projectiles if p.active]
