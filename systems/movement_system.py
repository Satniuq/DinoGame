# systems/movement_system.py

class MovementSystem:
    def update(self, world, dt):
        world.player.update()

        for e in world.enemies:
            e.update()

        for o in world.obstacles:
            o.update()

        for p in world.player.projectiles:
            p.update()
