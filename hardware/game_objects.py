from abc import ABC, abstractmethod
from typing import Dict

from utils import Coordinate, Color, ColorEnum
import random

GRAVITY = -2
MAX_X = 300
MAX_Y = 200
MAX_RADIUS_PERCENT = 0.05
MIN_RADIUS_PERCENT = 0.01
MAX_X_VELOCITY = 4
MIN_X_VELOCITY = 1
MAX_Y_VELOCITY = 50
MIN_Y_VELOCITY = 30

class Entity(ABC):
    position: Coordinate
    x_velocity: float
    y_velocity: float
    radius: float
    color: Color

    def __init__(self) -> None:
        self.position = Coordinate(random.random()*MAX_X, -20)
        on_left_side = self.position.x < MAX_X/2
        self.x_velocity = (1 if on_left_side else -1) * (random.random()*MAX_X_VELOCITY + MIN_X_VELOCITY)
        self.y_velocity = random.random()*MAX_Y_VELOCITY + MIN_Y_VELOCITY
        self.radius = random.random()*(MAX_RADIUS_PERCENT * MAX_X) + (MIN_RADIUS_PERCENT * MAX_X)
        self.color = ColorEnum.MAGENTA.value

    def map_to_display(self) -> Dict[int, Color]:
        leds: Dict[int, Color] = dict()

        for y_coord in range(int(self.position.y - self.radius), int(self.position.y + self.radius), 10):
            for x_coord in range(int(self.position.x - self.radius), int(self.position.x + self.radius), 10):
                distance: float = ((self.position.x - x_coord)**2 + (self.position.y - y_coord)**2)**(0.5)
                inEntity = distance <= self.radius

                if inEntity:
                    led_position = Coordinate(x_coord, y_coord).convert_xy_to_linear()
                    leds[led_position] = self.color
        return leds

    def next_position(self):
        self.position.x += self.x_velocity
        self.position.y += self.y_velocity

        self.y_velocity += GRAVITY

        print("fruit at", self.position.x, self.position.y, "velocity", self.y_velocity)


class Fruit(Entity):
    point_value: int
    sliced: bool

    def __init__(self, point_value):
        super().__init__()
        self.point_value = point_value
        self.color = ColorEnum.GREEN.value

    def handle_slice(self) -> list:
        #TODO: when sliced, returns two half fruits with opposite velocities
        ...

class Bomb(Entity):
    life_penalty: int

    def __init__(self, life_penalty):
        super().__init__()
        self.life_penalty = life_penalty
        self.color = ColorEnum.RED.value
