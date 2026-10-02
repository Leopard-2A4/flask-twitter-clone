import logging

from models.database import db
from models.users import User
from models.tweets import Tweet
from models.follows import Follow
from models.likes import Like
from models.media import Media
from configuration import create_app


def create_test_data():
    """Создаёт тестовых пользователей и твиты для проверки API."""

    app = create_app()
    app.logger.setLevel(logging.INFO)

    with app.app_context():
        try:
            db.session.query(Like).delete()
            db.session.query(Follow).delete()
            db.session.query(Media).delete()
            db.session.query(Tweet).delete()
            db.session.query(User).delete()
            db.session.commit()

            user1 = User(name="test")
            user2 = User(name="user2")

            db.session.add_all([user1, user2])
            db.session.commit()

            tweet1 = Tweet(
                content="Первый тестовый твит от test",
                author_id=user1.id
            )

            tweet2 = Tweet(
                content="Второй тестовый твит от user2",
                author_id=user2.id
            )

            db.session.add_all([tweet1, tweet2])
            db.session.commit()

            app.logger.info("Пользователи созданы:")
            app.logger.info("  - %s (id=%s)", user1.name, user1.id)
            app.logger.info("  - %s (id=%s)", user2.name, user2.id)

            app.logger.info("Твиты созданы:")
            app.logger.info("  - %s... (id=%s, author=%s)", tweet1.content[:40], tweet1.id, tweet1.author_id)
            app.logger.info("  - %s... (id=%s, author=%s)", tweet2.content[:40], tweet2.id, tweet2.author_id)

            app.logger.info("Тестовые данные успешно созданы!")
            app.logger.info("Для тестирования используйте api-key: test")

        except Exception:
            app.logger.exception("Ошибка при создании тестовых данных")
            raise


if __name__ == "__main__":
    create_test_data()