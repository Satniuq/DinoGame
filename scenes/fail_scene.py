# scenes/fail_scene.py
import pygame
from scenes.base_scene import BaseScene
from settings import WIDTH, HEIGHT, WHITE

class FailScene(BaseScene):
    def __init__(self, scene_manager, level):
        super().__init__(scene_manager)
        self.level = level
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                from scenes.play_scene import PlayScene
                # reinicia no mesmo nível
                self.scene_manager.change_scene(
                    PlayScene(self.scene_manager, self.level)
                )

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(WHITE)

        title = self.font.render(
            "GAME OVER",
            True,
            (200, 0, 0),
        )
        hint = self.small_font.render(
            "Pressiona R para tentar novamente",
            True,
            (0, 0, 0),
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40),
        )
        screen.blit(
            hint,
            (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20),
        )
