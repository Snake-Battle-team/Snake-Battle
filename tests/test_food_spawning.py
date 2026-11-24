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
from game.contracts import Direction
from game.food_spawning import replenish_food
from game.game_state import GameState
from game.snake import Snake


class FoodSpawningTests(unittest.TestCase):
    """Check where food is placed on the board."""

    def setUp(self) -> None:
        """Start each test with two snakes and an empty food list."""
        self.state = GameState(
            board=Board(4, 2),
            player=Snake([(1, 0), (0, 0)], Direction.RIGHT),
            AI=Snake([(2, 0), (3, 0)], Direction.LEFT),
            foods=[],
        )

    def test_initial_food_uses_three_distinct_free_cells(self) -> None:
        """Place three food items inside the board and clear of both snakes."""
        replenish_food(self.state)

        positions = {food.position for food in self.state.foods}
        occupied = set(self.state.player.body + self.state.AI.body)

        self.assertEqual(len(self.state.foods), 3)
        self.assertEqual(len(positions), 3)
        self.assertTrue(positions.isdisjoint(occupied))
        for position in positions:
            self.assertTrue(self.state.board.is_inside(position))