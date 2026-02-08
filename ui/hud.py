import pygame

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen, level_def, progress, player, score=None):
        resolved = progress.killed + progress.passed

        txt = (
            f"Nível {level_def.level} | "
            f"Vidas: {player.lives} | "
            f"Spawned: {progress.spawned}/{level_def.total_air_enemies} | "
            f"Mortos: {progress.killed} | "
            f"Passaram: {progress.passed} | "
            f"Resolvidos: {resolved}/{level_def.total_air_enemies}"
        )

        surf = self.font.render(txt, True, (0, 0, 0))
        screen.blit(surf, (10, 10))

        if score is not None:
            score_surf = self.font.render(
                f"Score: {int(score)}",
                True,
                (0, 0, 0),
            )
            screen.blit(score_surf, (10, 35))
