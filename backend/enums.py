import enum


class GameEvent(enum.Enum):
    FRUIT_SLICED = 'FRUIT_SLICED'
    BOMB_SLICED = 'BOMB_SLICED'
    GAME_START = 'GAME_START'
    GAME_END = 'GAME_END'
