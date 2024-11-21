from datetime import datetime
from game_objects import Fruit, Bomb
from utils import Coordinate

# import board
# import neopixel

class GameMetadata:
    fruits: list[Fruit]
    bombs: list[Bomb]
    cursor: list[Coordinate]
    frame_num: int
    game_id: int
    total_game_length: int
    last_render_timestamp: float
    fps: int
    num_points: int
    num_lives: int
    game_type: int

    # LED_STRIP: neopixel.NeoPixel

    events_to_post: list

    def __init__(self, game_id: int, num_lives: int, total_game_length: int, game_type: int) -> None:
        self.fruits = []
        self.bombs = []
        self.cursor = []
        self.frame_num = 0
        self.game_id = game_id
        self.total_game_length = total_game_length
        self.last_render_timestamp = datetime.now().timestamp()
        self.fps = 10
        self.num_points = 0
        self.num_lives = num_lives
        self.game_type = game_type

        # self.LED_STRIP = neopixel.NeoPixel(board.D18, 600)


    def print_game_state():
        # TODO: print the LED representation of fruits and bombs for debugging
        ...
