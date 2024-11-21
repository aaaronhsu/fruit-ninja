from typing import Tuple
from datetime import datetime
import time

import hardware_io
import game_logic
import network
import utils

from game_metadata import GameMetadata
from utils import Coordinate
from network import fetch_current_game

FPS: int = 10
FRAME_TIME: float = 1.0 / FPS  # Time per frame in seconds

class Driver:
    current_game: GameMetadata
    last_render_time: float  # Track when we last rendered a frame

    def __init__(self):
        self.last_render_time = 0.0

    def blocking_start_game(self) -> None:
        while not (self.current_game := fetch_current_game()):
            time.sleep(1)
        self.last_render_time = time.time()  # Initialize render timing

    def should_render_frame(self) -> bool:
        current_time = time.time()
        time_since_last_render = current_time - self.last_render_time

        if time_since_last_render >= FRAME_TIME:
            self.last_render_time = current_time  # Update last render time
            return True
        return False

    def run_game(self) -> bool: # returns False if the game is over
        # TODO: fetch the current_live_game and check that this corresponds to the current game data

        cursor_position: Coordinate = hardware_io.fetch_cursor()

        self.current_game = game_logic.calculate_next_game_state(
            current_state=self.current_game,
            cursor=cursor_position
        )

        if self.should_render_frame():
            hardware_io.render(self.current_game, cursor_position)

        return True # this should be False if the game is over

    def end_game(self) -> GameMetadata:
        # TODO: mark the game as over, clear current game and return it
        ...


if __name__ == "__main__":
    game_driver = Driver()
    # TODO: use Driver class to run the game

    game_driver.blocking_start_game()

    while True:
        game_driver.run_game()

    # game: GameMetadata = GameMetadata(
    #     game_id=-1,
    #     num_lives=10,
    #     total_game_length=100,
    #     game_type=0
    # )

    # game.led_strip[100] = (255, 255, 255)
    # # while 1:
    # #     pos: Coordinate = hardware_io.fetch_cursor()
    # #     print(pos.x, pos.y)
