from typing import TypedDict


class Pieces(TypedDict):
    R: str
    G: str
    B: str


class GameState(TypedDict):
    players: list[str]
    status: str
    turn: str
    moves: list[str]
    moves_left: int | None
    pieces: Pieces
