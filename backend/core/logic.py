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
