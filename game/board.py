
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
    """Represent the rectangular grid where the snakes move.

    Attributes:
        width (int): Number of columns on the board.
        height (int): Number of rows on the board.
    """

    def __init__(self, width: int, height: int):
        """Create a board with the given dimensions.

        Args:
            width (int): Number of columns.
            height (int): Number of rows.

        Raises:
            ValueError: If either dimension is zero or negative.
        """
        if width <= 0 or height <= 0:
            raise ValueError(
                "Board dimensions must be positive."
            )

        self.width = width
        self.height = height

    def is_inside(self, position: Position) -> bool:
        """Check whether a cell is within the board boundaries.

        Args:
            position (Position): Cell coordinates as (x, y), where x is
                the column and y is the row. Both start at zero.

        Returns:
            bool: True if x is between 0 and width - 1 and y is between
                0 and height - 1, inclusive. Otherwise, False.
        """
        x, y = position

        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )
