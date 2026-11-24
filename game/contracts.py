
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
    """Represent a one-cell move as a (dx, dy) offset.

    Moving right increases the column. Moving down increases the row.
    """

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameStatus(Enum):
    """Represent the current stage or final result of a match.

    READY means the match is waiting to start. During RUNNING, both
    snakes can move. PAUSE suspends movement until play resumes.

    PLAYER_WIN and AI_WIN identify the surviving snake. DRAW means
    both snakes were eliminated during the same turn.
    """
    
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSE = "PAUSE"
    PLAYER_WIN = "PLAYER_WIN"
    AI_WIN = "AI_WIN"
    DRAW = "DRAW"
