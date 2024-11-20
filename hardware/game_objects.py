from abc import ABC, abstractmethod
from typing import Dict

from utils import Coordinate, Color, ColorEnum

GRAVITY = -1

class Entity(ABC):
    position: Coordinate
    x_velocity: float
    y_velocity: float
    radius: int
    color: Color

    def __init__(self) -> None:
        # TODO: Randomize values
        position = Coordinate(0, 0)
        x_velocity = 5
        y_velocity = 3
        radius = 1

    def map_to_display() -> Dict[int, Color]:
        # TODO:
        # create a dictionary that maps the current entity to LED positions and Colors
        # fetch the LED position from Coordinate.convert_xy_to_linear()
        # use ColorEnum.RED.value, ColorEnum.GREENvalue, etc. for default pixel colors
        ...

    def next_position(self):
        self.position.x += self.x_velocity
        self.position.y += self.y_velocity

        self.y_velocity += GRAVITY


class Fruit(Entity):
    point_value: int
    sliced: bool

    def __init__(self, point_value):
        super().__init__()
        self.point_value = point_value
        self.color = ColorEnum.GREEN.value

class Bomb(Entity):
    life_penalty: int

    def __init__(self, life_penalty):
        super().__init__()
        self.life_penalty = life_penalty
        self.color = ColorEnum.RED.value
