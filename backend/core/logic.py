from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import GameState


def move_is_valid(move: str) -> bool:
    if len(move) != 3:
        return False

    colour = move[0]
    file_letter = move[1]
    rank_number = move[2]

    return (
        colour in ("r", "g", "b")
        and file_letter in "abcdefgh"
        and rank_number in "12345678"
    )


def set_moves_for_game(game: GameState, moves: int) -> None:
    game["moves_left"] = moves
