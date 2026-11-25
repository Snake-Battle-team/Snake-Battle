"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from game.board import Board
from game.contracts import Direction, GameStatus
from game.food_spawning import replenish_food
from game.game_state import GameState
from game.snake import Snake


class Game:
    """Manage the state and controls of a Snake Battle match.

    Attributes:
        width (int): Width of the board.
        height (int): Height of the board.
        state (GameState): Current state of the match.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize a new match.

        Args:
            width (int): Width of the board.
            height (int): Height of the board.
        """
        if width < 4 or height < 2:
            raise ValueError("Board is too small for two snakes.")

        self.width = width
        self.height = height
        self.state = self._create_match()

    def _create_match(self) -> GameState:
        """Create the initial board, snakes, and food."""
        board = Board(self.width, self.height)

        player = Snake([(1, 0), (0, 0)], Direction.RIGHT)

        opponent = Snake(
            [
                (self.width - 2, self.height - 1),
                (self.width - 1, self.height - 1),
            ],
            Direction.LEFT,
        )

        state = GameState(
            board=board,
            player=player,
            AI=opponent,
            foods=[],
        )

        replenish_food(state)

        return state

    def start(self) -> None:
        """Change a ready match to RUNNING."""
        if self.state.status == GameStatus.READY:
            self.state.status = GameStatus.RUNNING

    def pause(self) -> None:
        """Pause the match if it is running."""
        if self.state.status == GameStatus.RUNNING:
            self.state.status = GameStatus.PAUSE

    def resume(self) -> None:
        """Resume a paused match without changing its components."""
        if self.state.status == GameStatus.PAUSE:
            self.state.status = GameStatus.RUNNING

    def restart(self) -> None:
        """Create a new match with the initial state."""
        self.state = self._create_match()