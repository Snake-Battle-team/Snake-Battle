"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

import unittest

from game.contracts import Direction
from game.snake import Snake


class SnakeMovementTests(unittest.TestCase):
    """Check how a snake plans its next move on the board."""

    def setUp(self) -> None:
        """Create a two-segment snake facing right before each test."""
        self.snake = Snake([(3, 2), (2, 2)], Direction.RIGHT)

    def test_forward_move_advances_one_cell(self) -> None:
        """Continuing right places the next head one cell to the right."""
        move = self.snake.plan_move(Direction.RIGHT)

        self.assertEqual(move, (Direction.RIGHT, (4, 2)))

    def test_turn_updates_both_direction_and_position_in_the_plan(self) -> None:
        """Turning up decreases the head's y coordinate by one."""
        move = self.snake.plan_move(Direction.UP)

        self.assertEqual(move, (Direction.UP, (3, 1)))

    def test_turn_into_neck_keeps_current_direction(self) -> None:
        """A request to enter the neck makes the snake continue forward."""
        move = self.snake.plan_move(Direction.LEFT)

        self.assertEqual(move, (Direction.RIGHT, (4, 2)))

    def test_single_segment_snake_can_reverse(self) -> None:
        """A snake with no neck can move into the cell behind its head."""
        snake = Snake([(3, 2)], Direction.RIGHT)

        move = snake.plan_move(Direction.LEFT)

        self.assertEqual(move, (Direction.LEFT, (2, 2)))

    def test_planning_preserves_body_and_direction(self) -> None:
        """The body and direction stay unchanged until the move is applied."""
        self.snake.plan_move(Direction.DOWN)

        self.assertEqual(self.snake.body, [(3, 2), (2, 2)])
        self.assertEqual(self.snake.direction, Direction.RIGHT)

    def test_normal_move_releases_the_tail(self) -> None:
        """A normal move releases the tail and preserves the original body."""
        projected = self.snake.project_body((4, 2))

        self.assertEqual(projected, [(4, 2), (3, 2)])
        self.assertEqual(self.snake.body, [(3, 2), (2, 2)])

    def test_growth_keeps_the_tail(self) -> None:
        """A growing move keeps the tail and preserves the original body."""
        projected = self.snake.project_body((4, 2), grow=True)

        self.assertEqual(projected, [(4, 2), (3, 2), (2, 2)])
        self.assertEqual(self.snake.body, [(3, 2), (2, 2)])