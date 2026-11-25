"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

import unittest

from game.contracts import GameStatus
from game.game import Game


class GameLifecycleTests(unittest.TestCase):
    """Check how a match starts, pauses, resumes, and restarts."""

    def setUp(self) -> None:
        """Create a new match before each test."""
        self.game = Game(8, 6)

    def test_new_match_starts_ready(self) -> None:
        """A new match starts with both snakes alive and zero scores."""
        state = self.game.state

        self.assertEqual(state.status, GameStatus.READY)
        self.assertEqual(state.player.score, 0)
        self.assertEqual(state.AI.score, 0)
        self.assertTrue(state.player.alive)
        self.assertTrue(state.AI.alive)

        self.assert_valid_positions()

    def test_start_changes_status_to_running(self) -> None:
        """Starting a ready match changes its status to RUNNING."""
        self.game.start()

        self.assertEqual(self.game.state.status, GameStatus.RUNNING)

    def test_pause_changes_status_to_pause(self) -> None:
        """A running match can be paused."""
        self.game.start()
        self.game.pause()

        self.assertEqual(self.game.state.status, GameStatus.PAUSE)

    def test_resume_preserves_match_state(self) -> None:
        """Resuming preserves the snakes, scores, and food."""
        self.game.start()

        state = self.game.state
        state.player.score = 2
        state.AI.score = 1

        player_body = state.player.body.copy()
        opponent_body = state.AI.body.copy()
        food_positions = [food.position for food in state.foods]

        self.game.pause()
        self.game.resume()

        self.assertIs(self.game.state, state)
        self.assertEqual(state.status, GameStatus.RUNNING)
        self.assertEqual(state.player.score, 2)
        self.assertEqual(state.AI.score, 1)
        self.assertEqual(state.player.body, player_body)
        self.assertEqual(state.AI.body, opponent_body)
        self.assertEqual(
            [food.position for food in state.foods],
            food_positions,
        )

    def test_restart_creates_a_new_match(self) -> None:
        """Restarting a finished match resets its components."""
        old_state = self.game.state

        old_state.status = GameStatus.PLAYER_WIN
        old_state.player.score = 5
        old_state.AI.score = 2
        old_state.AI.alive = False

        self.game.restart()

        state = self.game.state

        self.assertIsNot(state, old_state)
        self.assertIsNot(state.player, old_state.player)
        self.assertIsNot(state.AI, old_state.AI)
        self.assertIsNot(state.foods, old_state.foods)
        self.assertEqual(state.status, GameStatus.READY)
        self.assertEqual(state.player.score, 0)
        self.assertEqual(state.AI.score, 0)
        self.assertTrue(state.player.alive)
        self.assertTrue(state.AI.alive)

        self.assert_valid_positions()

    def test_invalid_transitions_preserve_status(self) -> None:
        """Invalid actions do not change the match status."""
        self.game.pause()
        self.game.resume()

        self.assertEqual(self.game.state.status, GameStatus.READY)

        self.game.state.status = GameStatus.DRAW
        self.game.start()

        self.assertEqual(self.game.state.status, GameStatus.DRAW)

    def assert_valid_positions(self) -> None:
        """Check that snakes and food occupy separate valid cells."""
        state = self.game.state

        positions = (
            state.player.body
            + state.AI.body
            + [food.position for food in state.foods]
        )

        self.assertEqual(len(state.foods), 3)
        self.assertEqual(len(positions), len(set(positions)))

        for position in positions:
            self.assertTrue(state.board.is_inside(position))