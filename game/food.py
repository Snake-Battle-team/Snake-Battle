
"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from game.contracts import Position


class Food:
    """Represent a single food item on the board.

    Attributes:
        position (Position): Cell occupied by the food item.
    """
    def __init__(self, position: Position):
        """Place the food item at the given coordinates.

        Args:
            position (Position): Board cell as a (column, row) pair.
        """
        self.position = position