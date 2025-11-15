import uuid
from typing import TYPE_CHECKING

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

if TYPE_CHECKING:
    from core.models import GameState

app = Flask(__name__)
_ = CORS(app)

games: dict[str, GameState] = {}


@app.route("/api/games", methods=["GET"])
def get_games() -> Response:
    return jsonify(games)


@app.route("/api/create_game", methods=["POST"])
def create_game() -> Response:
    game_id: str = str(uuid.uuid4())
    games[game_id] = {
        "players": [],
        "status": "waiting",
        "turn": "",
        "moves": [],
        "moves_left": 0,
        "pieces": {"R": "", "G": "", "B": ""},
    }
    return jsonify({"gameId": game_id, "game": games[game_id]})


@app.route("/api/join_game", methods=["POST"])
def join_game() -> tuple[Response, int]:
    data: dict[str, str] | None = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    game_id = data.get("gameId")
    player_name = data.get("player")

    if game_id is None or player_name is None:
        return jsonify({"error": "Invalid JSON"}), 400
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    current_game: GameState = games[game_id]

    if len(current_game["players"]) == 3:
        return jsonify({"error": "Game full"}), 403

    if player_name not in current_game["players"]:
        current_game["players"].append(player_name)
        if len(current_game["players"]) == 3:
            current_game["status"] = "ongoing"
            current_game["turn"] = current_game["players"][0]

    return jsonify(
        {
            "gameId": game_id,
            "players": current_game["players"],
            "status": current_game["status"],
        }
    ), 200


@app.route("/api/move", methods=["POST"])
def make_move() -> tuple[Response, int]:
    data: dict[str, str] | None = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    game_id: str | None = data.get("gameId")
    player_name: str | None = data.get("player")
    move: str | None = data.get("move")

    if game_id is None or player_name is None or move is None:
        return jsonify({"error": "Invalid JSON"}), 400
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    current_game: GameState = games[game_id]

    if current_game["status"] != "ongoing":
        return jsonify({"error": "Game has not begun"}), 403
    if player_name not in current_game["players"]:
        return jsonify({"error": "Invalid player name"}), 400

    players: list[str] = current_game["players"]

    if player_name == current_game["turn"]:
        current_game["moves"].append(move)
        current_game["moves_left"] -= 1
        if current_game["moves_left"] <= 0:
            current_game["turn"] = current_game["players"][
                (players.index(current_game["turn"]) + 1) % len(players)
            ]
            current_game["moves_left"] = 6

    return jsonify(
        {
            "gameId": game_id,
            "player": player_name,
            "nextPlayer": current_game["turn"],
            "moves": current_game["moves"],
            "movesLeft": current_game["moves_left"],
        }
    ), 200


@app.route("/api/set_moves", methods=["POST"])
def set_moves() -> tuple[Response, int]:
    data: dict[str, str] | None = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    game_id: str | None = data.get("gameId")
    num_moves: str | None = data.get("numMoves")

    if game_id is None or num_moves is None:
        return jsonify({"error": "Invalid JSON"}), 400
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
    if not num_moves.isdigit():
        return jsonify({"error": "Invalid JSON"}), 400

    moves: int = int(num_moves)
    if moves <= 0:
        return jsonify({"error": "Invalid JSON"}), 400

    current_game: GameState = games[game_id]
    current_game["moves_left"] = moves
    return jsonify({"gameId": game_id, "movesLeft": moves}), 200
