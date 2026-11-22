"""
Team 6 - Snake Battle
Computer Sciences I
Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

# Imported only for type hints, so the UI has no runtime dependency on the game logic layer.
if TYPE_CHECKING:
    from game.food import Food
    from game.game_state import GameState
    from game.snake import Snake

Color = tuple[int, int, int]
Direction = tuple[int, int]

RGBA = tuple[int,int, int]

# Board layout (the final board size is still to be defined by the team)
CELL_SIZE = 30
HUD_HEIGHT = 50
FPS = 60

# Colors (R, G, B) of the design
COLOR_BACKGROUND: Color = (15, 15, 20)
COLOR_GRID: Color = (28, 28, 36)
COLOR_WALL: Color = (40, 90, 200)
COLOR_PLAYER_BODY: Color = (60, 200, 80)
COLOR_PLAYER_HEAD: Color = (140, 255, 150)
COLOR_AI_BODY: Color = (220, 140, 40)
COLOR_AI_HEAD: Color = (255, 200, 110)
COLOR_FOOD: Color = (230, 40, 40)
COLOR_TEXT: Color = (235, 235, 235)

# Directions as (x, y). The y axis grows downwards on the screen.
UP: Direction = (0, -1)
DOWN: Direction = (0, 1)
LEFT: Direction = (-1, 0)
RIGHT: Direction = (1, 0)

# Keys that move the player's snake (arrows and WASD)
KEY_BINDINGS: dict[int, Direction] = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}

STEP_INTERVAL_MS = 175  # Time between game updates, in milliseconds

# Overlay screens (start, pause, result)
COLOR_OVERLAY: RGBA = (0, 0, 0, 160)    # The last value is the opacity
COLOR_PANEL: Color = (30, 30, 45)
PANEL_WIDTH = 360
PANEL_HEIGHT = 240
STATUS_RUNNING = "RUNNING"

# Title shown on the overlay for each game status
SCREEN_TITLES: dict[str, str] = {
    "READY": "Snake Battle",
    "PAUSE": "Paused",
    "PLAYER_WIN": "You win!",
    "AI_WIN": "The AI wins!",
    "DRAW": "Draw!",
}

@dataclass
class PlayerInput:
    """What the player asked for during one call to UI.read_input.

    Attributes:
        quit (bool): True if the player closed the window or pressed ESC.
        direction (Direction | None): Last direction key pressed, or None
            if no direction key was pressed.
        toggle_pause (bool): True if the player pressed the pause key (P).
    """

    quit: bool = False
    direction: Direction | None = None
    toggle_pause: bool = False

def status_name(state: GameState) -> str:
    """Return the game status as a plain string.

    Works whether the logic stores the status as a string or as an Enum.

    Args:
        state (GameState): Current game state.

    Returns:
        str: Status name, for example "RUNNING" or "PAUSE".
    """
    return getattr(state.status, "name", state.status)

class UI:
    """Building the interface using Pygame. This implementation does not define game rules; it is created solely by reading the game state (GameState).

    Attributes:
        board_width (int): It represents the width of the board
        board_height (int): It represents the height of the board
        width (int): Window width, in pixels.
        height (int): Window height in pixels, including the HUD bar.
        screen (pygame.Surface): Window surface where everything is drawn.
        clock (pygame.time.Clock): Clock used to limit the frame rate.
        font (pygame.font.Font): Font used to render the HUD text.
    """    

    def __init__(self, board_width, board_height) -> None:
        """Initialize Pygame and create the game window.

        Args:
            board_width (int): It represents the width of the board
            board_height (int): It represents the height of the board
        """        
        self.board_width = board_width
        self.board_height = board_height
        self.width = board_width * CELL_SIZE
        self.height = board_height * CELL_SIZE + HUD_HEIGHT

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Battle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 22)
        self.tittle_font = pygame.font.SysFont("arial", 40, bold=True)
        self._last_step_ms = 0

    def cell_rect (self, x, y):
        """Covert a board cell into a pixel rectangle

        Args:
            x (int): Horizontal cell coordinate
            y (int): Vertical cell cordinate

        Returns:
            _type_: _description_
        """        

        return pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def read_input(self) -> PlayerInput:
        """Read the pending keyboard and window events.

        The UI only reports what the player asked for. Whether a direction
        is allowed (for example, reversing into the own body) is a game
        rule and is decided by the game logic, not here.

        Returns:
            PlayerInput: Requested direction, pause toggle and quit flag.
        """
        result = PlayerInput()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result.quit = True
                elif event.key == pygame.K_p:
                    result.toggle_pause = True
                elif event.key in KEY_BINDINGS:
                    # If several keys arrive at once, the last one wins
                    result.direction = KEY_BINDINGS[event.key]
        return result

    def step_due(self) -> bool:
        """Tell whether it is time to run one game update.

        Drawing runs at FPS frames per second, but the snakes must move
        much slower, once every STEP_INTERVAL_MS milliseconds.

        Returns:
            bool: True if enough time has passed since the last update.
        """
        now = pygame.time.get_ticks()
        if now - self._last_step_ms >= STEP_INTERVAL_MS:
            self._last_step_ms = now
            return True
        return False

    def draw(self, state) -> None:
        """Draw one complete frame from the given state.

        Args:
            state (GameState): _description_
        """        

        self.screen.fill(COLOR_BACKGROUND)
        self.draw_grid()
        self.draw_foods(state.foods)

        self.draw_snake(state.player, COLOR_PLAYER_BODY, COLOR_PLAYER_HEAD)
        self.draw_snake(state.AI, COLOR_AI_BODY, COLOR_AI_HEAD)
        self.draw_walls()
        self.draw_hud(state)
        self.draw_screen(state)
        pygame.display.flip()

    def draw_screen(self, state: GameState) -> None:
        """Draw the overlay screen that matches the game status.

        Nothing is drawn while the game is running.

        Args:
            state (GameState): Current game state, read for its status.
        """
        if status_name(state) == STATUS_RUNNING:
            return
        panel = self.draw_overlay()
        title = SCREEN_TITLES.get(status_name(state), "")
        self.draw_text(title, self.tittle_font, (panel.centerx, panel.top + 50))

    def draw_text(self, text: str, font: pygame.font.Font, center: tuple[int, int]) -> None:
        """Draw a text centered on the given pixel.

        Args:
            text (str): Text to draw.
            font (pygame.font.Font): Font used to render the text.
            center (tuple[int, int]): Pixel (x, y) where the text is centered.
        """

        image = font.render(text, True, COLOR_TEXT)
        self.screen.blit(image, image.get_rect(center=center))

    def draw_overlay(self) -> pygame.Rect:
        """Darken the whole window and draw a centered panel on top.

        Returns:
            pygame.Rect: The panel, so callers can place content inside it.
        """
        # SRCALPHA lets the surface be semi-transparent
        shade = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        shade.fill(COLOR_OVERLAY)
        self.screen.blit(shade, (0, 0))

        panel = pygame.Rect(0, 0, PANEL_WIDTH, PANEL_HEIGHT)
        panel.center = (self.width // 2, self.height // 2)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_WALL, panel, 3, border_radius=12)
        return panel

    def draw_grid(self) -> None:
        """Draw the border of every board cell to form the grid
        """        
        for x in range(self.board_width):
            for y in range(self.board_height):
                pygame.draw.rect(self.screen, COLOR_GRID, self.cell_rect(x, y), 1)

    def draw_foods(self, foods) -> None:
        """Draw every food as a circle centered in its cell.

        Args:
            foods (Iterable[Food]): Foods currently on the board
        """        
        for food in foods:
            x, y = food.position
            center = self.cell_rect(x, y).center
            pygame.draw.circle(self.screen, COLOR_FOOD, center, CELL_SIZE // 2 - 3)

    def draw_snake(self, snake, body_color, head_color) -> None:
        """Draw a snake segment by segment

        Args:
            snake (Snake): Snake to draw. Its body has the head at index 0.
            body_color (Color): Color of the body segments.
            head_color (Color): Color of the head segment.
        """        
        for index, (x, y) in enumerate(snake.body):
            color = head_color if index == 0 else body_color
            rect = self.cell_rect(x,y).inflate(-4, -4)
            pygame.draw.rect(self.screen, color, rect, border_radius=6)

    def draw_walls(self) -> None:
        """Draw the border around the board.

        This is only visual. Deciding whether a snake hit the wall is
        the job of the game logic.
        """        
        area = (0, 0, self.board_width * CELL_SIZE, self.board_height * CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_WALL, area, 4)

    def draw_hud(self, state) -> None:
        """Draw the bottom bar with the score and length of each snake.

        The player text is aligned to the left and the AI text to the
        right.

        Args:
            sstate (GameState): Current game state, read for the score and body length of player and AI.
        """        
        top = self.board_height*CELL_SIZE
        pygame.draw.rect(self.screen, COLOR_WALL, (0, top, self.width, HUD_HEIGHT))
        player_text = f"Player: {state.player.score} (length{len(state.player.body)})"
        ai_text = f"AI: {state.AI.score}(length{len(state.AI.body)})"
        self.screen.blit(self.font.render(player_text, True, COLOR_TEXT), (10, top + 14))
        ai_image = self.font.render(ai_text, True, COLOR_TEXT)
        self.screen.blit(ai_image, (self.width - ai_image.get_width()-10, top + 14))