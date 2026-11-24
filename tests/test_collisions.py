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
from game.collisions import resolve_collisions
from game.contracts import GameStatus


class CollisionTests(unittest.TestCase):
    """Check the match outcome after both snakes plan their moves."""

    def setUp(self) -> None:
        """Create a five-by-five board for each collision scenario."""
        self.board = Board(5, 5)

    def test_both_snakes_survive_a_clear_move(self) -> None:
        """Keep the match running when both heads reach free cells."""
        player_body = [(1, 1), (0, 1)]
        ai_body = [(3, 3), (4, 3)]

        result = resolve_collisions(self.board, player_body, ai_body)

        self.assertEqual(result, GameStatus.RUNNING)

    def test_player_leaves_the_board(self) -> None:
        """Award the win to the AI when the player crosses the right edge."""
        player_body = [(5, 1), (4, 1)]
        ai_body = [(2, 3), (3, 3)]

        result = resolve_collisions(self.board, player_body, ai_body)

        self.assertEqual(result, GameStatus.AI_WIN)

    def test_ai_hits_its_own_body(self) -> None:
        """Award the win to the player when the AI runs into itself."""
        player_body = [(0, 0), (1, 0)]
        ai_body = [(2, 2), (2, 3), (3, 3), (3, 2), (2, 2)]

        result = resolve_collisions(self.board, player_body, ai_body)

        self.assertEqual(result, GameStatus.PLAYER_WIN)

    def test_player_hits_the_opponents_body(self) -> None:
        """Award the win to the AI when the player hits an opponent segment."""
        player_body = [(2, 2), (2, 1)]
        ai_body = [(3, 2), (2, 2), (1, 2)]

        result = resolve_collisions(self.board, player_body, ai_body)

        self.assertEqual(result, GameStatus.AI_WIN)

    def test_both_heads_reach_the_same_cell(self) -> None:
        """Declare a draw when both heads reach the same cell."""
        player_body = [(2, 2), (1, 2)]
        ai_body = [(2, 2), (3, 2), (4, 2)]

        result = resolve_collisions(self.board, player_body, ai_body)

        self.assertEqual(result, GameStatus.DRAW)

    def test_both_snakes_hit_different_obstacles(self) -> None:
        """Declare a draw when both snakes crash separately in one step."""
        player_body = [(5, 1), (4, 1)]
        ai_body = [(2, 2), (2, 3), (3, 3), (3, 2), (2, 2)]

        result = resolve_collisions(self.board, player_body, ai_body)

        self.assertEqual(result, GameStatus.DRAW)