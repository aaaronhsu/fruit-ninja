from datetime import datetime
import enum

from game_metadata import GameMetadata

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

    @staticmethod
    def post_events(events: list[Event]):
        # post events using the POST /api/events endpoint
        ...

def fetch_current_game() -> GameMetadata:
    # get and build current game info using the GET /api/current_game endpoint
    ...

def end_current_game(game_state: GameMetadata) -> None
    # make end game request using the POST /api/end_game endpoint
    ...
