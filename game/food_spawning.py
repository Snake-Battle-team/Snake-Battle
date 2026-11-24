"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from random import sample

from game.food import Food
from game.game_state import GameState


MAX_FOODS = 3


def replenish_food(state: GameState) -> None:
    """Add food on free cells until the board holds up to three items.

    Args:
        state (GameState): Current match state. New food is appended to
            its food list, preserving the positions of existing items.
    """
    missing = MAX_FOODS - len(state.foods)
    if missing <= 0:
        return

    occupied = set(state.player.body)
    occupied.update(state.AI.body)
    occupied.update(food.position for food in state.foods)

    free_cells = [
        (x, y)
        for y in range(state.board.height)
        for x in range(state.board.width)
        if (x, y) not in occupied
    ]

    count = min(missing, len(free_cells))
    for position in sample(free_cells, count):
        state.foods.append(Food(position))