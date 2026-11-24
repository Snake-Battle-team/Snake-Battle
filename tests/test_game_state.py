"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

import unittest

from game.board import Board
from game.contracts import Direction, GameStatus
from game.food import Food
from game.game_state import GameState
from game.snake import Snake


class GameStateTests(unittest.TestCase):
    """Check how the board, snakes, food, and status are stored together."""

    def test_new_match_exposes_its_components_and_starts_ready(self) -> None:
        """A new match exposes the supplied game objects and defaults to READY."""
        board = Board(8, 6)
        player = Snake([(1, 1), (0, 1)], Direction.RIGHT)
        opponent = Snake([(6, 4), (7, 4)], Direction.LEFT)
        foods = [Food((3, 1)), Food((4, 3)), Food((2, 5))]

        state = GameState(board=board, player=player, AI=opponent, foods=foods)

        self.assertIs(state.board, board)
        self.assertIs(state.player, player)
        self.assertIs(state.AI, opponent)
        self.assertEqual(state.foods, foods)
        self.assertEqual(state.status, GameStatus.READY)