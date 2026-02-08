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
    def __init__(self, manager, level=1, player_name="Jogador"):
        super().__init__(manager)

        # 🎮 Identidade e score
        self.player_name = player_name
        self.score = 0.0

        # 📈 Nível actual
        self.current_level = level

        # 🔌 Core do jogo
        self.bus = EventBus()
        self.world = World()
        self.world.player = Player()

        # 🌍 Definição e progresso do nível
        self.level_def = LevelDefinition(level=self.current_level)
        self.progress = LevelProgress()

        # ⚙️ Sistemas
        self.input = InputSystem()
        self.movement = MovementSystem()
        self.spawn = SpawnSystem(self.level_def)
        self.collision = CollisionSystem(self.bus)
        self.combat = CombatSystem(self.bus, self.world.player, self.progress)
        self.level = LevelSystem(self.bus, self.level_def, self.progress)
        self.lifetime = LifetimeSystem()

        # 📡 Eventos
        self.bus.subscribe(PlayerDied, self.on_player_died)
        self.bus.subscribe(LevelCompleted, self.on_level_completed)

        # 🖥️ HUD
        self.hud = HUD()

    def handle_event(self, event):
        self.input.handle(event, self.world)

    def update(self, dt):
        # ⏱️ Score por tempo sobrevivido
        self.score += dt

        self.spawn.update(self.world, self.progress)
        self.movement.update(self.world, dt)
        self.collision.update(self.world)
        self.lifetime.update(self.world)
        self.level.update()

    def draw(self, screen):
        screen.fill(WHITE)

        # chão
        pygame.draw.line(
            screen,
            (150, 150, 150),
            (0, GROUND_Y),
            (WIDTH, GROUND_Y),
            2,
        )

        # obstáculos
        for o in self.world.obstacles:
            o.draw(screen)

        # inimigos
        for e in self.world.enemies:
            e.draw(screen)

        # jogador
        self.world.player.draw(screen)

        # HUD (score pode ser integrado depois)
        self.hud.draw(
            screen,
            self.level_def,
            self.progress,
            self.world.player,
            self.score,
        )


    # ☠️ MORTE DO JOGADOR
    def on_player_died(self, event):
        self.scene_manager.change_scene(
            FailScene(
                self.scene_manager,
                self.current_level,
                self.player_name,
                self.score,
            )
        )

    # 🏁 FIM DO NÍVEL
    def on_level_completed(self, event):
        ratio = self.progress.killed / self.level_def.total_air_enemies

        if ratio >= self.level_def.min_kill_ratio:
            self.scene_manager.change_scene(
                WinScene(
                    self.scene_manager,
                    self.current_level,
                    self.player_name,
                    self.score,
                )
            )
        else:
            self.scene_manager.change_scene(
                FailScene(
                    self.scene_manager,
                    self.current_level,
                    self.player_name,
                    self.score,
                )
            )
