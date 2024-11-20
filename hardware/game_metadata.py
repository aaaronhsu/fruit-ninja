from datetime import datetime
from game_objects import Fruit, Bomb
from network import Event
from utils import Coordinate

class GameMetadata:
    fruits: list[Fruit]
    bombs: list[Bomb]
    cursor: list[Coordinate]
    frame_num: int
    game_id: int
    total_game_length: int
    last_render_timestamp: float
    fps: int

    events_to_post: list[Event]

    def print_game_state():
        # TODO: print the LED representation of fruits and bombs for debugging
        ...
