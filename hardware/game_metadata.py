from datetime import datetime
from game_objects import Fruit, Bomb
from utils import Coordinate
from collections import deque

import board
import neopixel

class GameMetadata:
    fruits: list[Fruit]
    bombs: list[Bomb]
    cursors: deque[Coordinate]
    frame_num: int
    game_id: int
    total_game_length: int
    last_render_timestamp: float
    fps: int
    num_points: int
    num_lives: int
    game_type: int

    events_to_post: list

    def __init__(self, game_id: int, num_lives: int, total_game_length: int, game_type: int) -> None:
        self.fruits = []
        self.bombs = []
        self.cursors = deque()
        self.frame_num = 0
        self.game_id = game_id
        self.total_game_length = total_game_length
        self.last_render_timestamp = datetime.now().timestamp()
        self.fps = 8
        self.num_points = 0
        self.num_lives = num_lives
        self.game_type = game_type

        self.events_to_post = []

        self.led_strip = neopixel.NeoPixel(board.D18, 600, auto_write=False)

    def print_game_state(self, render_radius: bool = False):
        """
        Prints ASCII representation of the game state for debugging
        Args:
            render_radius: If True, renders the full radius of fruits/bombs
        """
        # Create a 30x20 grid to match LED layout (x = 30 wide, y = 20 high)
        grid = [[' ' for x in range(30)] for y in range(20)]

        # Map fruits to grid
        for fruit in self.fruits:
            if render_radius:
                # Convert radius to grid units
                grid_radius = int((fruit.radius / 300) * 29)
                center_x = int((fruit.position.x / 300) * 29)
                center_y = int((fruit.position.y / 200) * 19)

                # Fill in all points within radius
                for dx in range(-grid_radius, grid_radius + 1):
                    for dy in range(-grid_radius, grid_radius + 1):
                        grid_x = center_x + dx
                        grid_y = center_y + dy

                        # Check if point is within circular radius and grid bounds
                        if (dx**2 + dy**2 <= grid_radius**2 and
                            0 <= grid_x < 30 and
                            0 <= grid_y < 20):
                            grid[19-grid_y][grid_x] = 'F'  # Invert y for display
            else:
                # Just render center point
                grid_x = int((fruit.position.x / 300) * 29)
                grid_y = int((fruit.position.y / 200) * 19)
                if 0 <= grid_x < 30 and 0 <= grid_y < 20:
                    grid[19-grid_y][grid_x] = 'F'  # Invert y for display

        # Map bombs to grid
        for bomb in self.bombs:
            if render_radius:
                grid_radius = int((bomb.radius / 300) * 29)
                center_x = int((bomb.position.x / 300) * 29)
                center_y = int((bomb.position.y / 200) * 19)

                for dx in range(-grid_radius, grid_radius + 1):
                    for dy in range(-grid_radius, grid_radius + 1):
                        grid_x = center_x + dx
                        grid_y = center_y + dy

                        if (dx**2 + dy**2 <= grid_radius**2 and
                            0 <= grid_x < 30 and
                            0 <= grid_y < 20):
                            grid[19-grid_y][grid_x] = 'B'  # Invert y for display
            else:
                grid_x = int((bomb.position.x / 300) * 29)
                grid_y = int((bomb.position.y / 200) * 19)
                if 0 <= grid_x < 30 and 0 <= grid_y < 20:
                    grid[19-grid_y][grid_x] = 'B'  # Invert y for display

        # Map cursors to grid with trail
        for i, cursor in enumerate(self.cursors):
            grid_x = int((cursor.x / 300) * 29)
            grid_y = int((cursor.y / 200) * 19)
            if 0 <= grid_x < 30 and 0 <= grid_y < 20:
                # Use different characters for cursor trail: C -> c -> .
                cursor_char = 'C' if i == 0 else ('c' if i == 1 else '.')
                grid[19-grid_y][grid_x] = cursor_char

        # Print game stats
        print(f"\nGame ID: {self.game_id}")
        print(f"Lives: {self.num_lives}")
        print(f"Points: {self.num_points}")
        print(f"Frame: {self.frame_num}")
        print(f"Fruits: {len(self.fruits)}, Bombs: {len(self.bombs)}")
        print(f"Cursor positions: {[(c.x, c.y) for c in self.cursors]}\n")

        # Print grid with border
        print("+" + "-" * 30 + "+")
        for row in grid:
            print("|" + "".join(row) + "|")
        print("+" + "-" * 30 + "+")
