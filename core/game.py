# core/game.py
import pygame
from core.scene_manager import SceneManager
from scenes.play_scene import PlayScene
from settings import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Prototype")

        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager()
        self.scene_manager.change_scene(PlayScene(self.scene_manager))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene_manager.handle_event(event)

            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)

            pygame.display.flip()
