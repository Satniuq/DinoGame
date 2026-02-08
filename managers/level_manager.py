# managers/level_manager.py
from settings import *


class LevelManager:
    def __init__(self, level=1):
        self.level = level
        self.configure_level()

    # ------------------
    def configure_level(self):
        """
        Configuração declarativa do nível.
        Aqui define-se:
        - objetivos
        - dificuldade base
        - rewards
        """

        # -------- OBJETIVOS --------
        self.total_air_enemies = 20 + (self.level - 1) * 5
        self.min_kill_ratio = max(0.4, 0.6 - self.level * 0.02)

        # -------- ESTATÍSTICAS --------
        self.spawned_air = 0
        self.killed_air = 0
        self.passed_air = 0

        # -------- SCORE --------
        self.base_score_per_kill = 100
        self.level_bonus = self.level * 250

        # -------- DIFICULDADE (exposta para outros managers) --------
        self.speed_multiplier = 1.0 + (self.level - 1) * 0.15
        self.spawn_pressure = min(1.0, 0.6 + self.level * 0.05)

        # -------- ESTADO --------
        self.enemies = []

    # ==================
    # PROPRIEDADES
    # ==================
    @property
    def resolved_air(self):
        return self.killed_air + self.passed_air

    @property
    def kill_ratio(self):
        if self.total_air_enemies == 0:
            return 0.0
        return self.killed_air / self.total_air_enemies

    @property
    def score(self):
        """
        Score total do nível.
        """
        return (
            self.killed_air * self.base_score_per_kill
            + self.level_bonus
        )

    # ==================
    # ESTADO DO NÍVEL
    # ==================
    def is_finished(self):
        """
        O nível termina quando todos os inimigos obrigatórios
        foram mortos OU passaram.
        """
        return self.resolved_air >= self.total_air_enemies

    def is_won(self):
        """
        Vitória depende da taxa mínima de kills.
        """
        return self.kill_ratio >= self.min_kill_ratio

    # ==================
    # EVENTOS
    # ==================
    def enemy_killed(self, enemy):
        from entities.enemies import AirEnemy
        if isinstance(enemy, AirEnemy):
            self.killed_air += 1

    def enemy_passed(self, enemy):
        from entities.enemies import AirEnemy
        if isinstance(enemy, AirEnemy):
            self.passed_air += 1

    # ==================
    # PROGRESSÃO
    # ==================
    def next_level(self):
        self.level += 1
        self.configure_level()
