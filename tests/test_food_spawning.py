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
from game.food import Food


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

    def test_replenishment_preserves_remaining_food(self) -> None:
        """Keep the two remaining food items and add one on a free cell."""
        self.state.foods = [Food((0, 1)), Food((1, 1))]

        replenish_food(self.state)

        positions = {food.position for food in self.state.foods}
        self.assertEqual(len(self.state.foods), 3)
        self.assertIn((0, 1), positions)
        self.assertIn((1, 1), positions)
        self.assertEqual(len(positions & {(2, 1), (3, 1)}), 1)