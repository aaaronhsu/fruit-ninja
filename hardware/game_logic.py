import random
import copy

from game_metadata import GameMetadata
from game_objects import Entity, Bomb, Fruit
from network import Event
from utils import Coordinate
from network import Event, GameEvent

def spawn_fruit() -> Fruit:
    return Fruit(10)

def spawn_bomb() -> Bomb:
    return Bomb(1)

def handle_possible_collision(object: Entity, cursor: Coordinate) -> Event | None:
    def is_collision() -> bool:
        distance: float = ((object.position.x - cursor.x)**2 + (object.position.y - cursor.y)**2)**(0.5)
        return distance < object.radius

    if not is_collision():
        return None

    if isinstance(object, Fruit):
        metadata = {
            "points": object.point_value
        }

        return Event(GameEvent.FRUIT_SLICED, metadata)
    elif isinstance(object, Bomb):
        metadata = {
            "lives": -object.life_penalty
        }
        return Event(GameEvent.BOMB_SLICED, metadata)

def despawn_fallen_entities(current_state: GameMetadata) -> None:
    current_state.fruits = [fruit for fruit in current_state.fruits 
        if not (fruit.position.y < -40 and fruit.y_velocity < 0)]
    current_state.bombs = [bomb for bomb in current_state.bombs 
        if not (bomb.position.y < -40 and bomb.y_velocity < 0)]

def calculate_next_game_state(current_state: GameMetadata, cursor: Coordinate) -> GameMetadata:
    next_game_state: GameMetadata = copy.deepcopy(current_state)

    # calculate next position for all entities
    for entity in next_game_state.fruits + next_game_state.bombs:
        entity.next_position()

        # handle collision event
        sliced_event = handle_possible_collision(entity, cursor)
        if sliced_event:
            next_game_state.events_to_post.append(sliced_event)
    
    despawn_fallen_entities(next_game_state)

    # spawn new entities
    if random.random() < 0.02:
        new_fruit = spawn_fruit()
        next_game_state.fruits.append(new_fruit)
    if random.random() < 0.005:
        new_bomb = spawn_bomb()
        next_game_state.bombs.append(new_bomb)

    return next_game_state