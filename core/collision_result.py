# core/collision_result.py
from enum import Enum


class CollisionResult(Enum):
    AIR_KILLED = 1
    PLAYER_HIT = 2
