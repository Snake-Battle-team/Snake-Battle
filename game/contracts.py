
"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from enum import Enum
from typing import Tuple


Position = Tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameStatus(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSE = "PAUSE"
    PLAYER_WIN = "PLAYER_WIN"
    AI_WIN = "AI_WIN"
    DRAW = "DRAW"
