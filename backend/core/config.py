import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

COLOURS: list[str] = ["r", "g", "b"]
MAX_MOVES: int = 6

_ = load_dotenv()

SECRET_KEY: str | None = os.getenv("SECRET_KEY")
DEBUG: bool = os.getenv("DEBUG", "false") == "true"
FRONTEND_URL: str = os.getenv("FRONTEND_URL", "127.0.0.1:5173")

app = Flask(__name__)
_ = CORS(app, origins=[FRONTEND_URL])

if SECRET_KEY is not None:
    app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = DEBUG
