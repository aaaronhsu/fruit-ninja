from abc import ABC, abstractmethod
from typing import Dict
import enum

from utils import Coordinate, Color, ColorEnum
import random
from datetime import datetime

GRAVITY = -5
MAX_X = 300
MAX_Y = 200
MAX_RADIUS_PERCENT = 0.05
MIN_RADIUS_PERCENT = 0.01
MAX_X_VELOCITY = 8
MIN_X_VELOCITY = 3
MAX_Y_VELOCITY = 25
MIN_Y_VELOCITY = 20

class GameEvent(str, enum.Enum):
    FRUIT_SLICED = 'FRUIT_SLICED'
    BOMB_SLICED = 'BOMB_SLICED'
    GAME_START = 'GAME_START'
    GAME_END = 'GAME_END'

class Event:
    type: GameEvent
    game_id: int
    timestamp: float
    metadata: dict

    def __init__(
        self,
        type: GameEvent,
        metadata: dict
    ) -> None:
        self.type = type
        self.timestamp = datetime.now().timestamp()
        self.metadata = metadata

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
        # self.radius = random.random()*(MAX_RADIUS_PERCENT * MAX_X) + (MIN_RADIUS_PERCENT * MAX_X)
        self.radius = 20
        self.color = ColorEnum.MAGENTA.value

    def map_to_display(self) -> Dict[int, Color]:
        leds: Dict[int, Color] = dict()

        for y_coord in range(int(self.position.y - self.radius), int(self.position.y + self.radius), 10):
            for x_coord in range(int(self.position.x - self.radius), int(self.position.x + self.radius), 10):
                distance: float = ((self.position.x - x_coord)**2 + (self.position.y - y_coord)**2)**(0.5)
                inEntity = distance <= self.radius

                if inEntity:
                    led_position = Coordinate(x_coord, y_coord).convert_xy_to_linear()
                    if led_position:
                        leds[led_position] = self.color
        return leds

    def next_position(self):
        self.position.x += self.x_velocity
        self.position.y += self.y_velocity

        self.y_velocity += GRAVITY

        # print("fruit at", self.position.x, self.position.y, "velocity", self.y_velocity)

    @abstractmethod
    def handle_slice(self) -> Event | None:
        pass


class Fruit(Entity):
    point_value: int
    sliced: bool

    def __init__(self, point_value):
        super().__init__()
        self.point_value = point_value
        self.color = ColorEnum.GREEN.value

    def handle_slice(self) -> Event | None:
        print("sliced fruit")
        metadata = {
            "points": self.point_value
        }
        return Event(GameEvent.FRUIT_SLICED, metadata)


class Bomb(Entity):
    life_penalty: int

    def __init__(self, life_penalty):
        super().__init__()
        self.life_penalty = life_penalty
        self.color = ColorEnum.RED.value

    def handle_slice(self) -> Event | None:
        print("sliced bomb")
        metadata = {
            "lives": -self.life_penalty
        }
        return Event(GameEvent.BOMB_SLICED, metadata)
