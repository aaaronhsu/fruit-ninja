from typing import Tuple
from dataclasses import dataclass
from enum import Enum

@dataclass
class Coordinate:
    x: float
    y: float

    def convert_xy_to_linear(self) -> int:
        # TODO: converts coordinate to LED position

        # idea is that we have a 20 x 30 grid of LEDs 
        # 0-29
        # 59-30
        # 60-89
        # 118-90
        # 119-148
        # 178-149
        # 179-

        #coordinates occupy a 200 x 300 space, as if it is a 2d array 
        #0  .......... 299
        #   ..........
        #   ..........
        #199 .......... 
        ...


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