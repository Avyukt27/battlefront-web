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

    if game_id is None:
        return jsonify({"error": "Invalid game id"}), 400

    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    if len(games[game_id]["players"]) == 3:
        return jsonify({"error": "Game full"}), 403

    if player_name is None:
        return jsonify({"error": "Invalid player name"}), 400

    if player_name not in games[game_id]["players"]:
        games[game_id]["players"].append(player_name)
        if len(games[game_id]["players"]) == 3:
            games[game_id]["status"] = "ongoing"
            games[game_id]["turn"] = games[game_id]["players"][0]

    return jsonify(
        {
            "gameId": game_id,
            "players": games[game_id]["players"],
            "status": games[game_id]["status"],
        }
    ), 200


@app.route("/api/leave_game", methods=["POST"])
def leave_game() -> tuple[Response, int]:
    data: dict[str, str] | None = request.json

    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    game_id: str | None = data.get("gameId")
    player_name: str | None = data.get("player")

    if game_id is None:
        return jsonify({"error": "Invalid game id"}), 400

    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    if player_name is None:
        return jsonify({"error": "Invalid player name"}), 400

    if player_name in games[game_id]["players"]:
        games[game_id]["players"].remove(player_name)

    return jsonify({"gameId": game_id, "players": games[game_id]["players"]}), 200


@app.route("/api/move", methods=["POST"])
def make_move() -> tuple[Response, int]:
    data: dict[str, str] | None = request.json

    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    game_id: str | None = data.get("gameId")
    player_name: str | None = data.get("player")
    move: str | None = data.get("move")

    if game_id is None:
        return jsonify({"error": "Invalid game id"}), 400

    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    if player_name is None or player_name not in games[game_id]["players"]:
        return jsonify({"error": "Invalid player name"}), 400

    if move is None:
        return jsonify({"error": "Invalid move"}), 400

    if player_name == games[game_id]["turn"]:
        games[game_id]["moves"].append(move)
        games[game_id]["turn"] = games[game_id]["players"][
            (games[game_id]["players"].index(games[game_id]["turn"]) + 1) % 3
        ]

    return jsonify(
        {
            "gameId": game_id,
            "player": player_name,
            "nextPlayer": games[game_id]["turn"],
            "moves": games[game_id]["moves"],
        }
    ), 200
