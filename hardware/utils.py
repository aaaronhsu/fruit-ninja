from typing import Tuple
from dataclasses import dataclass
from enum import Enum

@dataclass
class Coordinate:
    x: float
    y: float

    def convert_xy_to_linear(self) -> int:
        # First, map the x,y coordinates to grid positions
        # Map x from (0,300) to (0,29)
        grid_x = int((self.x / 300) * 29)
        # Map y from (0,200) to (0,19)
        grid_y = int((self.y / 200) * 19)

        # Clamp values to ensure they're within bounds
        grid_x = max(0, min(29, grid_x))
        grid_y = max(0, min(19, grid_y))

        # For even rows (0,2,4...), LEDs go left to right
        # For odd rows (1,3,5...), LEDs go right to left
        if grid_y % 2 == 0:
            # Even row - left to right
            led_position = grid_y * 30 + grid_x
        else:
            # Odd row - right to left
            led_position = grid_y * 30 + (29 - grid_x)

        return led_position


class Color:
    r: int
    g: int
    b: int

    def __init__(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue

    def apply_to_led_strip(self, led_num: int, pixels) -> None:
        # TODO: applies color to led_num to pixels
        # if 0 <= led_num <= 599:
        pixels[led_num] = (self.r, self.g, self.b)

class ColorEnum(Enum):
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    YELLOW = Color(255, 255, 0)
    MAGENTA = Color(255, 0, 255)
    CYAN = Color(0, 255, 255)
    GRAY = Color(128, 128, 128)
    PURPLE = Color(128, 0, 128)
    ORANGE = Color(255, 165, 0)
    PINK = Color(255, 192, 203)
    BROWN = Color(165, 42, 42)
    SILVER = Color(192, 192, 192)
    GOLD = Color(255, 215, 0)
