
"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from game.contracts import Position


class Board:
    def __init__(self, width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValueError(
                "Board dimensions must be positive."
            )

        self.width = width
        self.height = height

    def is_inside(self, position: Position) -> bool:
        x, y = position

        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )
