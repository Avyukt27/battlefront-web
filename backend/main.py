import uuid

from flask import Flask, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
_ = CORS(app)

games: dict[str, dict[str, str | list[str]]] = {}


@app.route("/api/games", methods=["GET"])
def get_games() -> Response:
    return jsonify(games)


@app.route("/api/create_game", methods=["POST"])
def create_game() -> Response:
    game_id: str = str(uuid.uuid4())

    games[game_id] = {
        "players": [],
        "state": "waiting",
        "moves": [],
    }

    return jsonify({"gameId": game_id, "game": games[game_id]})


if __name__ == "__main__":
    app.run(debug=True)
