# scenes/fail_scene.py

import pygame
from scenes.base_scene import BaseScene
from settings import WIDTH, HEIGHT, WHITE
from data.highscore_repository import add_score

class FailScene(BaseScene):
    def __init__(self, scene_manager, level, player_name, score):
        super().__init__(scene_manager)

        self.level = level
        self.player_name = player_name
        self.score = score

        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

        # 🏆 guarda score no ranking
        add_score(player_name, score)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                from scenes.play_scene import PlayScene
                self.scene_manager.change_scene(
                    PlayScene(
                        self.scene_manager,
                        self.level,
                        self.player_name
                    )
                )

            elif event.key == pygame.K_m:
                from scenes.menu_scene import MenuScene
                self.scene_manager.change_scene(
                    MenuScene(self.scene_manager)
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

        score_text = self.small_font.render(
            f"Score: {int(self.score)}",
            True,
            (0, 0, 0),
        )

        hint = self.small_font.render(
            "R - tentar novamente | M - menu",
            True,
            (0, 0, 0),
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80),
        )
        screen.blit(
            score_text,
            (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20),
        )
        screen.blit(
            hint,
            (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 40),
        )
