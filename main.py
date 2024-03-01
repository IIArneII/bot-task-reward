from fastapi import FastAPI
from uvicorn import run

from app.app import create_app
from app.config import Config


app: FastAPI | None = None


def main(config: Config):
    global app
    app = create_app(config)


if __name__ == 'main':
    main(Config())


if __name__ == '__main__':
    config = Config()
    main(config)
    run(app, host=config.app.HOST, port=config.app.PORT)
