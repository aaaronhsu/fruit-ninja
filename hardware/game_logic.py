import random
import copy

from game_metadata import GameMetadata
from game_objects import Entity, Bomb, Fruit, Event, GameEvent
from utils import Coordinate


def spawn_fruit() -> Fruit:
    return Fruit(10)


def spawn_bomb() -> Bomb:
    return Bomb(1)


def handle_possible_collision(current_state: GameMetadata, object: Entity, cursor: Coordinate) -> Event | None:
    def is_collision() -> bool:
        distance: float = ((object.position.x - cursor.x)**2 + (object.position.y - cursor.y)**2)**(0.5)
        return distance < object.radius

    if is_collision():
        return object.handle_slice(current_state)
    return None


def despawn_fallen_entities(current_state: GameMetadata) -> None:
    current_state.fruits = [fruit for fruit in current_state.fruits
        if not (fruit.position.y < -40 and fruit.y_velocity < 0)]
    current_state.bombs = [bomb for bomb in current_state.bombs
        if not (bomb.position.y < -40 and bomb.y_velocity < 0)]


def calculate_next_game_state(current_state: GameMetadata, cursor: Coordinate) -> GameMetadata:
    next_game_state: GameMetadata = copy.deepcopy(current_state)

    next_game_state.cursors.appendleft(cursor)
    if len(next_game_state.cursors) > 3:
        next_game_state.cursors.pop()

    # calculate next position for all entities
    for entity in next_game_state.fruits + next_game_state.bombs:
        entity.next_position()

        # handle collision event
        sliced_event: Event | None = handle_possible_collision(next_game_state, entity, cursor)
        if sliced_event:
            next_game_state.events_to_post.append(sliced_event)

    despawn_fallen_entities(next_game_state)

    # spawn new entities
    if random.random() < 0.08:
        new_fruit = spawn_fruit()
        next_game_state.fruits.append(new_fruit)
    if random.random() < 0.03:
        new_bomb = spawn_bomb()
        next_game_state.bombs.append(new_bomb)

    next_game_state.frame_num += 1

    return next_game_state
