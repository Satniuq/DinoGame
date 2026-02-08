# scenes/play_scene.py
import pygame
from scenes.base_scene import BaseScene
from scenes.fail_scene import FailScene
from scenes.win_scene import WinScene

from world.world import World
from world.level_definition import LevelDefinition
from world.level_progress import LevelProgress

from core.events_bus import EventBus
from core.events import PlayerDied, LevelCompleted

from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.spawn_system import SpawnSystem
from systems.collision_system import CollisionSystem
from systems.combat_system import CombatSystem
from systems.level_system import LevelSystem
from systems.lifetime_system import LifetimeSystem

from ui.hud import HUD
from entities.player import Player
from settings import WHITE, WIDTH, GROUND_Y

class PlayScene(BaseScene):
    def __init__(self, manager, level=1):
        super().__init__(manager)

        self.current_level = level   # 👈 guarda o nível

        self.bus = EventBus()
        self.world = World()
        self.world.player = Player()

        # 👇 AGORA O NÍVEL É PASSADO
        self.level_def = LevelDefinition(level=self.current_level)
        self.progress = LevelProgress()

        self.input = InputSystem()
        self.movement = MovementSystem()
        self.spawn = SpawnSystem(self.level_def)
        self.collision = CollisionSystem(self.bus)
        self.combat = CombatSystem(self.bus, self.world.player, self.progress)
        self.level = LevelSystem(self.bus, self.level_def, self.progress)
        self.lifetime = LifetimeSystem()

        self.bus.subscribe(PlayerDied, self.on_player_died)
        self.bus.subscribe(LevelCompleted, self.on_level_completed)

        self.hud = HUD()

    def handle_event(self, event):
        self.input.handle(event, self.world)

    def update(self, dt):
        self.spawn.update(self.world, self.progress)
        self.movement.update(self.world, dt)
        self.collision.update(self.world)
        self.lifetime.update(self.world)
        self.level.update()

    def draw(self, screen):
        screen.fill(WHITE)

        pygame.draw.line(
            screen,
            (150, 150, 150),
            (0, GROUND_Y),
            (WIDTH, GROUND_Y),
            2,
        )

        for o in self.world.obstacles:
            o.draw(screen)

        for e in self.world.enemies:
            e.draw(screen)

        self.world.player.draw(screen)
        self.hud.draw(screen, self.level_def, self.progress, self.world.player)

    def on_player_died(self, event):
        # reinicia no mesmo nível
        self.scene_manager.change_scene(
            FailScene(self.scene_manager, self.current_level)
        )

    def on_level_completed(self, event):
        ratio = self.progress.killed / self.level_def.total_air_enemies
        if ratio >= self.level_def.min_kill_ratio:
            # AVANÇA DE NÍVEL 👇
            self.scene_manager.change_scene(
                WinScene(self.scene_manager, self.current_level)
            )
        else:
            self.scene_manager.change_scene(
                FailScene(self.scene_manager, self.current_level)
            )
