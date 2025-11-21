import os

from core.routes import app
from dotenv import load_dotenv

if __name__ == "__main__":
    _ = load_dotenv()

    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG", "false") == "true"

    if SECRET_KEY is not None:
        app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG

    app.run()
