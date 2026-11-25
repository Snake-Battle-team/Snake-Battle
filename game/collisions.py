"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from game.board import Board
from game.contracts import GameStatus, Position


def resolve_collisions(
    board: Board,
    player_body: list[Position],
    ai_body: list[Position],
) -> GameStatus:
    """Determine the match outcome from both snakes' projected bodies.

    Args:
        board (Board): Grid used to check whether a head is in bounds.
        player_body (list[Position]): Projected player segments, head first.
        ai_body (list[Position]): Projected opponent segments, head first.

    Returns:
        GameStatus: RUNNING if both survive, PLAYER_WIN or AI_WIN if one
            survives, or DRAW if both are eliminated during the same step.
    """
    player_head = player_body[0]
    ai_head = ai_body[0]

    if player_head == ai_head:
        return GameStatus.DRAW

    player_hit = (
        not board.is_inside(player_head)
        or player_head in player_body[1:]
        or player_head in ai_body[1:]
    )
    ai_hit = (
        not board.is_inside(ai_head)
        or ai_head in ai_body[1:]
        or ai_head in player_body[1:]
    )

    if player_hit and ai_hit:
        return GameStatus.DRAW
    if player_hit:
        return GameStatus.AI_WIN
    if ai_hit:
        return GameStatus.PLAYER_WIN
    return GameStatus.RUNNING