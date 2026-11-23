"""
Team 6 - Snake Battle
Computer Sciences I

Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from game.contracts import Direction, Position


class Snake:
    """Represent the current state of a player or AI snake.

    Attributes:
        body (list[Position]): Board cells occupied by the snake, ordered
            from head to tail. The head is at index 0.
        direction (Direction): Current direction of movement on the board.
        score (int): Points earned by eating food during the match.
        alive (bool): True while the snake is still active in the match.
    """

    def __init__(
        self,
        body: list[Position],
        direction: Direction,
        score: int = 0,
        alive: bool = True,
    ) -> None:
        """Initialize the snake with its body and direction of movement.

        Args:
            body (list[Position]): Initial segment positions, starting
                with the head and ending with the tail.
            direction (Direction): Initial direction of movement.
            score (int): Initial score. Defaults to 0.
            alive (bool): Whether the snake starts active. Defaults to True.

        Raises:
            ValueError: If the body has no segments.
        """
        if not body:
            raise ValueError("A snake must have at least one segment.")

        self.body = body.copy()
        self.direction = direction
        self.score = score
        self.alive = alive

    def plan_move(self, requested_direction: Direction) -> tuple[Direction, Position]:
        """Calculate the direction and next head position for one game step.

        Both snakes can plan their moves from the same board state before
        either body is updated.

        Args:
            requested_direction (Direction): Direction requested for this
                step. Pass the current direction to keep moving forward.

        Returns:
            tuple[Direction, Position]: The effective direction and the next
                head position. If the requested move would enter the neck,
                the snake continues in its current direction.
        """
        head_x, head_y = self.body[0]
        direction = requested_direction
        dx, dy = direction.value
        next_head = (head_x + dx, head_y + dy)

        if len(self.body) > 1 and next_head == self.body[1]:
            direction = self.direction
            dx, dy = direction.value
            next_head = (head_x + dx, head_y + dy)

        return direction, next_head

    def project_body(self, next_head: Position, grow: bool = False) -> list[Position]:
        """Calculate the cells the snake would occupy after one move.

        Args:
            next_head (Position): Head position returned by plan_move().
            grow (bool): Whether the tail stays in place during this move.
                Defaults to False.

        Returns:
            list[Position]: A new list of segments in head-to-tail order.
                The snake's current body remains unchanged.
        """
        projected = [next_head]
        projected.extend(self.body)
        if not grow:
            projected.pop()
        return projected