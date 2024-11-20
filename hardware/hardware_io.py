from typing import Dict

from game_metadata import GameMetadata
from utils import Color, Coordinate, Color
# import board
# import neopixel
# LED_STRIP = neopixel.NeoPixel(board.D18, 600)

def render(game_state: GameMetadata, cursor: Coordinate):
    leds_to_render: Dict[int, Color] = dict()

    # iterate through all entities and map them to LED positions
    for entity in game_state.fruits + game_state.bombs:
        leds_to_render.update(entity.map_to_display())

    # add white cursor
    leds_to_render.update({cursor.convert_xy_to_linear(): Color(255, 255, 255)})

    LED_STRIP.fill((0, 0, 0)) # flush the LED strip
    for (led_num, color) in leds_to_render.items():
        color.apply_to_led_strip(led_num, LED_STRIP)

    LED_STRIP.show()

def fetch_cursor() -> Coordinate:
    # fetches normalized cursor position using pixycam
    ...
