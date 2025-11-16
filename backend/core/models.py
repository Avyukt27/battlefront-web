from typing import TypedDict


class Piece(TypedDict):
    position: str
    has_ability: bool
    ability_cooldown: int | None
    piece_class: str


class Pieces(TypedDict):
    r: Piece
    g: Piece
    b: Piece


class Player(TypedDict):
    name: str
    colour: str


class GameState(TypedDict):
    players: list[Player]
    status: str
    turn: str
    moves: list[str]
    moves_left: int | None
    pieces: Pieces
