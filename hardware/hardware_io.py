from __future__ import print_function
import pixy
from ctypes import *
from pixy import *

from typing import Dict

from game_metadata import GameMetadata
from utils import Color, Coordinate, Color


def render(game_state: GameMetadata, cursor: Coordinate, debug=False):
    if debug:
        game_state.print_game_state(render_radius=True)
        return
    leds_to_render: Dict[int, Color] = dict()
    print(f"rendering frame {game_state.frame_num}")

    # add cursor path
    for cursor in game_state.cursors:
        cursor_led_id: int | None = cursor.convert_xy_to_linear()
        if cursor_led_id:
            leds_to_render.update({cursor_led_id: Color(100, 100, 100)})

    # iterate through all entities and map them to LED positions
    for entity in game_state.fruits + game_state.bombs:
        leds_to_render.update(entity.map_to_display())

    # apply actual cursor position
    cursor_led_id: int | None = cursor.convert_xy_to_linear()
    if cursor_led_id:
        leds_to_render.update({cursor_led_id: Color(255, 255, 255)})

    game_state.led_strip.fill((0, 0, 0)) # flush the LED strip
    for (led_num, color) in leds_to_render.items():
        color.apply_to_led_strip(led_num, game_state.led_strip)

    game_state.led_strip.show()


def fetch_cursor(game_state: GameMetadata, debug=False) -> Coordinate:
    # Initialize Pixy2 if not already initialized
    if debug:
        return Coordinate(150, 100)  # Center position as default
    pixy.init()
    pixy.change_prog("color_connected_components")

    # Create blocks array to store detected objects
    blocks = BlockArray(100)

    # Get blocks (detected objects)
    count = pixy.ccc_get_blocks(100, blocks)

    if count > 0:
        # Get the first detected object's position
        # blocks[0] contains the largest/most prominent detected object
        past_diffs = [0] * count

        for i in range(count):
            for cursor in game_state.cursors:
                past_diffs[i] += ( ((cursor.x - blocks[i].m_x)**2  + (cursor.y - blocks[i].m_y)**2)**0.5 )
        
        block_num = past_diffs.index(min(past_diffs))

        x = blocks[block_num].m_x
        y = blocks[block_num].m_y
    
        # Normalize coordinates
        # Pixy2 resolution is 316x208
        normalized_x = x / 316.0  # Convert to 0-1 range
        normalized_y = y / 208.0  # Convert to 0-1 range

        return Coordinate(normalized_x * 300, normalized_y * 200)
    else:
        # Return a default coordinate or handle no detection case
        # You might want to modify this based on your needs
        return Coordinate(-500, -500)  # Center position as default
