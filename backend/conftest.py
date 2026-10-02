import os
import sys
import tempfile
import shutil

sys.path.append(os.path.dirname(__file__))

import pytest

from configuration import create_app
from models.database import db
from models.users import User
from models.tweets import Tweet
from models.follows import Follow
from models.likes import Like
from models.media import Media


@pytest.fixture(scope="session")
def app():
    upload_dir = tempfile.mkdtemp(prefix="pytest_uploads_")

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_ECHO": False,
        "UPLOAD_FOLDER": upload_dir,
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

    shutil.rmtree(upload_dir, ignore_errors=True)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers():
    return {"api-key": "test"}


@pytest.fixture()
def seed_data(app):
    with app.app_context():
        db.session.query(Like).delete()
        db.session.query(Follow).delete()
        db.session.query(Media).delete()
        db.session.query(Tweet).delete()
        db.session.query(User).delete()
        db.session.commit()

        user1 = User(name="test")
        user2 = User(name="user2")
        db.session.add_all([user1, user2])
        db.session.flush()

        tweet1 = Tweet(content="Tweet from test", author_id=user1.id)
        tweet2 = Tweet(content="Tweet from user2", author_id=user2.id)
        db.session.add_all([tweet1, tweet2])
        db.session.flush()

        db.session.commit()

        return {
            "user1_id": user1.id,
            "user2_id": user2.id,
            "tweet1_id": tweet1.id,
            "tweet2_id": tweet2.id,
            "user1_name": user1.name,
            "user2_name": user2.name,
        }