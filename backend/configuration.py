from flask import Flask
from dotenv import load_dotenv
from models.database import db
from routes.start import init_routes
import os
import time
import logging
from sqlalchemy.exc import OperationalError

load_dotenv()

def init_swagger(app):
    from flasgger import Swagger
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Twitter Clone API",
            "version": "1.0"
        },
        "securityDefinitions": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "name": "api-key",
                "in": "header"
            }
        }
    }

    Swagger(
        app,
        template=swagger_template,
        config={
            "headers": [],
            "specs": [
                {
                    "endpoint": "apispec",
                    "route": "/apispec.json",
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True,
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/apidocs"
        }
    )

def init_db(app):
    with app.app_context():
        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            try:
                db.create_all()
                app.logger.info("База данных успешно создана")
                return
            except OperationalError:
                attempt += 1
                if attempt < max_attempts:
                    app.logger.warning(
                        "PostgreSQL ещё не готов. Попытка %s/%s. Пауза 2 секунды...",
                        attempt,
                        max_attempts
                    )
                    time.sleep(2)
                else:
                    app.logger.exception(
                        "Не удалось подключиться к PostgreSQL после %s попыток",
                        max_attempts
                    )
                    raise


def create_app(test_config=None):
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    if test_config is not None:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:postgres@postgres:5432/twitter_clone"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)
    init_routes(app)

    if test_config is None:
        init_db(app)
        init_swagger(app)


    return app