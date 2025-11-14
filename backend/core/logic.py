def move_is_valid(move: str, turn: str) -> bool:
    split_move: list[str] = list(move)
    return (
        split_move[0] == turn
        and split_move[1] in ["a", "bc", "d", "e", "f", "g", "h"]
        and split_move[2] in range(1, 9)
    )
