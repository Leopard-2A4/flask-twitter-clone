from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app):
    """
    Инициализирует базу данных для Flask приложения.

    Args:
        app: Flask приложение
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
