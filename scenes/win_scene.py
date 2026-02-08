# scenes/win_scene.py
import pygame
from scenes.base_scene import BaseScene
from settings import WIDTH, HEIGHT, WHITE

class WinScene(BaseScene):
    def __init__(self, scene_manager, level):
        super().__init__(scene_manager)
        self.level = level
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                from scenes.play_scene import PlayScene
                # 👇 PRÓXIMO NÍVEL
                self.scene_manager.change_scene(
                    PlayScene(self.scene_manager, self.level + 1)
                )
            elif event.key == pygame.K_r:
                from scenes.play_scene import PlayScene
                # reinicia do nível 1
                self.scene_manager.change_scene(
                    PlayScene(self.scene_manager, 1)
                )

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(WHITE)

        title = self.font.render(
            f"NÍVEL {self.level} CONCLUÍDO",
            True,
            (0, 150, 0),
        )
        hint1 = self.small_font.render(
            "N - próximo nível",
            True,
            (0, 0, 0),
        )
        hint2 = self.small_font.render(
            "R - reiniciar",
            True,
            (0, 0, 0),
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60),
        )
        screen.blit(
            hint1,
            (WIDTH // 2 - hint1.get_width() // 2, HEIGHT // 2),
        )
        screen.blit(
            hint2,
            (WIDTH // 2 - hint2.get_width() // 2, HEIGHT // 2 + 40),
        )
