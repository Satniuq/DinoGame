# systems/movement_system.py

class MovementSystem:
    def update(self, world, dt):
        world.player.update(dt)

        for e in world.enemies:
            if hasattr(e, "update"):
                try:
                    e.update(dt, world)
                except TypeError:
                    e.update(dt)

        for o in world.obstacles:
            o.update(dt)

        for p in world.player.projectiles:
            p.update(dt)

