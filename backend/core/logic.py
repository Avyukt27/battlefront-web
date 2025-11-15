def move_is_valid(move: str, turn: str, players: list[str]) -> bool:
    split_move: list[str] = list(move)
    currnt_colour: str = ["r", "g", "b"][players.index(turn)]
    print(currnt_colour, split_move, split_move[0] == currnt_colour)
    return (
        split_move[0] == currnt_colour
        and split_move[1] in ["a", "b", "c", "d", "e", "f", "g", "h"]
        and split_move[2] in ["1", "2", "3", "4", "5", "6", "7", "8"]
    )
