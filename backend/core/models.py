from typing import TypedDict


class Piece(TypedDict):
    position: str
    has_ability: bool
    ability_cooldown: int | None
    piece_class: str


class Pieces(TypedDict):
    red: Piece
    green: Piece
    blue: Piece


class GameState(TypedDict):
    players: list[str]
    status: str
    turn: str
    moves: list[str]
    moves_left: int | None
    pieces: Pieces
