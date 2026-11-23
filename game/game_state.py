"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from game.board import Board
from game.contracts import GameStatus
from game.food import Food
from game.snake import Snake


class GameState:
    """Store the shared state of a Snake Battle match.

    Attributes:
        board (Board): Grid where the match takes place.
        player (Snake): Snake controlled by the player.
        AI (Snake): Snake controlled by the opponent algorithm.
        foods (list[Food]): Food items currently on the board.
        status (GameStatus): Current match status.
    """

    def __init__(
        self,
        board: Board,
        player: Snake,
        AI: Snake,
        foods: list[Food],
        status: GameStatus = GameStatus.READY,
    ) -> None:
        """Initialize the state of a match.

        Args:
            board (Board): Board used by both snakes.
            player (Snake): Player-controlled snake.
            AI (Snake): AI-controlled snake.
            foods (list[Food]): Food items present at the start of this state.
            status (GameStatus): Match status. Defaults to READY.
        """
        self.board = board
        self.player = player
        self.AI = AI
        self.foods = foods
        self.status = status