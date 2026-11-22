"""
Team 6 - Snake Battle
Computer Sciences I
Miguel Angel Quintero Puentes
Brayan Esteban Bonilla Piñeros
Luis Felipe Zubieta Rincón
Suhayl Mariana Barrantes Alvarado
"""

import pygame

# Board layout (the final board size is still to be defined by the team)
CELL_SIZE = 30
HUD_HEIGHT = 50
FPS = 60

# Colors (R, G, B) of the design
COLOR_BACKGROUND = (15, 15, 20)
COLOR_GRID = (28, 28, 36)
COLOR_WALL = (40, 90, 200)
COLOR_PLAYER_BODY = (60, 200, 80)
COLOR_PLAYER_HEAD = (140, 255, 150)
COLOR_AI_BODY = (220, 140, 40)
COLOR_AI_HEAD = (255, 200, 110)
COLOR_FOOD = (230, 40, 40)
COLOR_TEXT = (235, 235, 235)

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

    def cell_rect (self, x, y):
        """Covert a board cell into a pixel rectangle

        Args:
            x (int): Horizontal cell coordinate
            y (int): Vertical cell cordinate

        Returns:
            _type_: _description_
        """        

        return pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)

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
        pygame.display.flip()

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