# scenes/menu_scene.py
import pygame
from scenes.base_scene import BaseScene
from scenes.play_scene import PlayScene

from data.player_repository import load_players, add_player
from data.highscore_repository import get_top_scores


class MenuScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 28)

        # 👤 jogadores
        self.players = load_players()
        self.selected_index = 0
        self.input_name = ""

        # 🏆 highscores
        self.highscores = get_top_scores()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        # navegar jogadores
        if event.key == pygame.K_UP:
            self.selected_index = max(0, self.selected_index - 1)

        elif event.key == pygame.K_DOWN:
            self.selected_index = min(
                len(self.players) - 1,
                self.selected_index + 1
            )

        # ENTER → jogar
        elif event.key == pygame.K_RETURN:
            self.start_game()

        # apagar nome
        elif event.key == pygame.K_BACKSPACE:
            self.input_name = self.input_name[:-1]

        # escrever nome novo
        else:
            if event.unicode.isprintable() and len(self.input_name) < 12:
                self.input_name += event.unicode

    def start_game(self):
        # se escreveu nome novo → cria jogador
        if self.input_name.strip():
            name = self.input_name.strip()
            add_player(name)
            self.players = load_players()
            self.selected_index = self.players.index(name)
            self.input_name = ""

        if not self.players:
            return

        name = self.players[self.selected_index]
        self.scene_manager.change_scene(
            PlayScene(
                self.scene_manager,
                level=1,
                player_name=name
            )
        )

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 20))

        # título
        title = self.font.render("DINO GAME", True, (255, 255, 255))
        screen.blit(
            title,
            (screen.get_width() // 2 - title.get_width() // 2, 40),
        )

        # -------------------
        # jogadores
        y = 120
        players_title = self.small_font.render("Jogadores:", True, (200, 200, 200))
        screen.blit(players_title, (80, y))
        y += 30

        for i, p in enumerate(self.players):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            prefix = "> " if i == self.selected_index else "  "
            txt = self.small_font.render(prefix + p, True, color)
            screen.blit(txt, (80, y))
            y += 24

        # novo jogador
        new_player = self.small_font.render(
            f"Novo jogador: {self.input_name or '_'}",
            True,
            (150, 150, 150),
        )
        screen.blit(new_player, (80, y + 10))

        # -------------------
        # comandos
        controls_title = self.small_font.render(
            "Comandos:",
            True,
            (200, 200, 200),
        )
        screen.blit(controls_title, (80, y + 50))

        controls = [
            "Saltar: SPACE / W / KP8",
            "Baixar: ↓ / S / KP2",
            "Disparar: F / KP0",
        ]

        cy = y + 80
        for c in controls:
            txt = self.small_font.render(c, True, (150, 150, 150))
            screen.blit(txt, (80, cy))
            cy += 22

        # -------------------
        # highscores
        y = 120
        hs_title = self.small_font.render("Top 10 Highscores:", True, (200, 200, 200))
        screen.blit(hs_title, (420, y))
        y += 30

        for i, h in enumerate(self.highscores):
            txt = self.small_font.render(
                f"{i+1}. {h['player']} - {h['score']}",
                True,
                (200, 200, 200),
            )
            screen.blit(txt, (420, y))
            y += 22

        # -------------------
        # hint
        hint = self.small_font.render(
            "↑ ↓ escolher | ENTER jogar | escrever nome para criar",
            True,
            (120, 120, 120),
        )
        screen.blit(
            hint,
            (screen.get_width() // 2 - hint.get_width() // 2, screen.get_height() - 40),
        )
