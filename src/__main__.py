from uvicorn import run
from app.create_app import create_app


if __name__ == "__main__":
    app = create_app()
    run(app, host="0.0.0.0", port=8000)
