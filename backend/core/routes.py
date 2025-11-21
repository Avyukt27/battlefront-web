import uuid
from random import randint
from typing import TYPE_CHECKING

from flask import Response, jsonify, request

from core.config import COLOURS, MAX_MOVES, app
from core.logic import move_is_valid

if TYPE_CHECKING:
    from core.models import GameState, Player


games: dict[str, GameState] = {}


@app.route("/api/games", methods=["GET"])
def get_games() -> tuple[Response, int]:
    return jsonify(games), 200


@app.route("/api/game/<string:game_id>", methods=["GET"])
def get_game(game_id: str) -> tuple[Response, int]:
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(games[game_id]), 200


@app.route("/api/create_game", methods=["POST"])
def create_game() -> tuple[Response, int]:
    game_id: str = str(uuid.uuid4())
    games[game_id] = {
        "players": [],
        "status": "waiting",
        "turn": "",
        "moves": [],
        "moves_left": None,
        "pieces": {
            "r": {
                "position": "",
                "has_ability": False,
                "ability_cooldown": None,
                "piece_class": "",
            },
            "g": {
                "position": "",
                "has_ability": False,
                "ability_cooldown": None,
                "piece_class": "",
            },
            "b": {
                "position": "",
                "has_ability": False,
                "ability_cooldown": None,
                "piece_class": "",
            },
        },
    }
    return jsonify({"gameId": game_id, "game": games[game_id]}), 201


@app.route("/api/join_game/<string:game_id>", methods=["POST"])
def join_game(game_id: str) -> tuple[Response, int]:
    data: dict[str, str] | None = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    player_name = data["player"]

    if not player_name:
        return jsonify({"error": "'player' field is missing"}), 400
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game: GameState = games[game_id]

    if len(game["players"]) == 3:
        return jsonify({"error": "Game full"}), 403
    if any(player["name"] == player_name for player in game["players"]):
        return jsonify({"error": "Player already joined"}), 403

    colour: str = COLOURS[len(game["players"])]

    game["players"].append({"name": player_name, "colour": colour})

    if len(game["players"]) == 3:
        game["status"] = "ongoing"
        game["turn"] = game["players"][0]["name"]
        game["pieces"]["r"]["position"] = "a8"
        game["pieces"]["g"]["position"] = "a1"
        game["pieces"]["b"]["position"] = "h1"
        game["moves_left"] = randint(1, MAX_MOVES)

    return jsonify(
        {
            "gameId": game_id,
            "players": game["players"],
            "status": game["status"],
        }
    ), 200


@app.route("/api/move/<string:game_id>", methods=["POST"])
def make_move(game_id: str) -> tuple[Response, int]:
    data: dict[str, str] | None = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    player_name: str | None = data.get("player")
    move: str | None = data.get("move")

    if not move:
        return jsonify({"error": "'move' field is missing"}), 400

    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game: GameState = games[game_id]

    if game["status"] != "ongoing":
        return jsonify({"error": "Game has not begun"}), 403
    if not game["moves_left"]:
        return jsonify({"error": "Moves not set"}), 400

    player: Player | None = next(
        (p for p in game["players"] if p["name"] == player_name), None
    )
    if not player:
        return jsonify({"error": "Invalid player name"}), 400
    if game["turn"] != player_name:
        return jsonify({"error": "Not your turn"}), 403
    if not move_is_valid(move):
        return jsonify({"error": "Invalid move"}), 403

    game["moves"].append(move)
    game["pieces"][player["colour"]]["position"] = move
    game["moves_left"] -= 1

    if game["moves_left"] <= 0:
        current_index: int = next(
            i for i, p in enumerate(game["players"]) if p["name"] == player_name
        )
        next_player = game["players"][(current_index + 1) % len(game["players"])][
            "name"
        ]

        game["turn"] = next_player
        game["moves_left"] = randint(1, MAX_MOVES)

    return jsonify(
        {
            "gameId": game_id,
            "player": player_name,
            "nextPlayer": game["turn"],
            "moves": game["moves"],
            "movesLeft": game["moves_left"],
        }
    ), 200


@app.route("/api/delete_game/<string:game_id>", methods=["DELETE"])
def delete_game(game_id: str) -> tuple[Response, int]:
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
    del games[game_id]
    return jsonify(games), 200
