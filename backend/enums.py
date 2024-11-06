import enum


class GameEvent(enum.Enum):
    FRUIT_SLICED = 'fruit_sliced'
    BOMB_SLICED = 'bomb_sliced'
    GAME_START = 'game_start'
    GAME_END = 'game_end'
