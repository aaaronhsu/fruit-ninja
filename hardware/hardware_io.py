from __future__ import print_function
import pixy
from ctypes import *
from pixy import *

from typing import Dict

from game_metadata import GameMetadata
from utils import Color, Coordinate, Color

def render(game_state: GameMetadata, cursor: Coordinate):
    leds_to_render: Dict[int, Color] = dict()

    # iterate through all entities and map them to LED positions
    for entity in game_state.fruits + game_state.bombs:
        leds_to_render.update(entity.map_to_display())

    # add white cursor
    # leds_to_render.update({cursor.convert_xy_to_linear(): Color(255, 255, 255)})

    game_state.led_strip.fill((0, 0, 0)) # flush the LED strip
    for (led_num, color) in leds_to_render.items():
        color.apply_to_led_strip(led_num, game_state.led_strip)

    game_state.led_strip.show()

def fetch_cursor() -> Coordinate:
    # Initialize Pixy2 if not already initialized
    pixy.init()
    pixy.change_prog("color_connected_components")

    # Create blocks array to store detected objects
    blocks = BlockArray(100)

    # Get blocks (detected objects)
    count = pixy.ccc_get_blocks(100, blocks)

    if count > 0:
        # Get the first detected object's position
        # blocks[0] contains the largest/most prominent detected object
        x = blocks[0].m_x
        y = blocks[0].m_y

        # Normalize coordinates
        # Pixy2 resolution is 316x208
        normalized_x = x / 316.0  # Convert to 0-1 range
        normalized_y = y / 208.0  # Convert to 0-1 range

        return Coordinate(normalized_x * 300, normalized_y * 200)
    else:
        # Return a default coordinate or handle no detection case
        # You might want to modify this based on your needs
        return Coordinate(-500, -500)  # Center position as default
