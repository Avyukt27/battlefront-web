def move_is_valid(move: str, turn: str, players: list[str]) -> bool:
    split_move: list[str] = list(move)
    currnt_colour: str = ["red", "green", "blue"][players.index(turn)]
    return (
        split_move[0] == currnt_colour
        and split_move[1] in ["a", "b", "c", "d", "e", "f", "g", "h"]
        and split_move[2] in range(1, 9)
    )
