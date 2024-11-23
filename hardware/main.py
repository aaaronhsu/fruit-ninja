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
DEBUG = True


class Driver:
    current_game: GameMetadata
    next_frame_time: float  # Track when next frame should be rendered

    def __init__(self):
        self.next_frame_time = 0.0

    def blocking_start_game(self) -> None:
        """Blocks until a game is fetched from the server"""
        self.current_game = fetch_current_game()
        while not self.current_game:
            self.current_game = fetch_current_game()
            time.sleep(1)
        self.next_frame_time = time.time()  # Initialize first frame time

    def wait_for_next_frame(self) -> None:
        """Blocks until it's time for the next frame"""
        if DEBUG:
            current_time = time.time()
            frame_delay = self.next_frame_time - current_time
            if frame_delay < 0:
                print(f"Frame overrun by {-frame_delay*1000:.1f}ms")
            else:
                print(f"Waiting {frame_delay*1000:.1f}ms for next frame")

        sleep_time = self.next_frame_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.next_frame_time += FRAME_TIME

    def run_game(self) -> bool:
        """Run one frame of the game"""
        cursor_position: Coordinate = hardware_io.fetch_cursor(debug=DEBUG)

        self.current_game = game_logic.calculate_next_game_state(
            current_state=self.current_game,
            cursor=cursor_position if not DEBUG else Coordinate(150, 100)
        )

        self.wait_for_next_frame()
        hardware_io.render(self.current_game, cursor_position, debug=DEBUG)

        return True

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
