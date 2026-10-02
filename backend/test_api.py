from io import BytesIO
import os
import sys

sys.path.append(os.path.dirname(__file__))

import pytest

from models.database import db
from models.users import User
from models.tweets import Tweet
from models.follows import Follow
from models.likes import Like
from models import Media


@pytest.fixture
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


def auth_headers():
    return {"api-key": "test"}


def test_follow_user_success(client, seed_data):
    response = client.post(f"/api/users/{seed_data['user2_id']}/follow", headers=auth_headers())
    assert response.status_code == 201
    assert response.get_json()["result"] is True


def test_follow_self_forbidden(client, seed_data):
    response = client.post(f"/api/users/{seed_data['user1_id']}/follow", headers=auth_headers())
    assert response.status_code == 400


def test_follow_missing_user(client):
    response = client.post("/api/users/999999/follow", headers=auth_headers())
    assert response.status_code == 404


def test_unfollow_user_success(client, seed_data):
    client.post(f"/api/users/{seed_data['user2_id']}/follow", headers=auth_headers())
    response = client.delete(f"/api/users/{seed_data['user2_id']}/follow", headers=auth_headers())
    assert response.status_code == 200
    assert response.get_json()["result"] is True


def test_unfollow_not_following(client, seed_data):
    response = client.delete(f"/api/users/{seed_data['user2_id']}/follow", headers=auth_headers())
    assert response.status_code == 400


def test_get_feed_returns_all_tweets(client, seed_data):
    response = client.get("/api/tweets", headers=auth_headers())
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] is True
    assert len(data["tweets"]) == 2


def test_get_feed_contains_both_authors(client, seed_data):
    response = client.get("/api/tweets", headers=auth_headers())
    assert response.status_code == 200
    data = response.get_json()
    authors = [tweet["author"]["name"] for tweet in data["tweets"]]
    assert seed_data["user1_name"] in authors
    assert seed_data["user2_name"] in authors


def test_get_my_profile_success(client, seed_data):
    response = client.get("/api/users/me", headers=auth_headers())
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] is True
    assert data["user"]["name"] == seed_data["user1_name"]


def test_get_user_profile_success(client, seed_data):
    response = client.get(f"/api/users/{seed_data['user2_id']}", headers=auth_headers())
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] is True
    assert data["user"]["name"] == seed_data["user2_name"]


def test_get_user_profile_missing_api_key(client, seed_data):
    response = client.get(f"/api/users/{seed_data['user2_id']}")
    assert response.status_code == 401


def test_get_user_profile_not_found(client):
    response = client.get("/api/users/999999", headers=auth_headers())
    assert response.status_code == 404


def test_add_like_success(client, seed_data):
    response = client.post(f"/api/tweets/{seed_data['tweet2_id']}/likes", headers=auth_headers())
    assert response.status_code == 201
    assert response.get_json()["result"] is True


def test_add_like_twice_forbidden(client, seed_data):
    tweet_id = seed_data["tweet2_id"]
    first = client.post(f"/api/tweets/{tweet_id}/likes", headers=auth_headers())
    assert first.status_code == 201
    second = client.post(f"/api/tweets/{tweet_id}/likes", headers=auth_headers())
    assert second.status_code == 400


def test_add_like_tweet_not_found(client):
    response = client.post("/api/tweets/999999/likes", headers=auth_headers())
    assert response.status_code == 404


def test_remove_like_success(client, seed_data):
    tweet_id = seed_data["tweet2_id"]
    client.post(f"/api/tweets/{tweet_id}/likes", headers=auth_headers())
    response = client.delete(f"/api/tweets/{tweet_id}/likes", headers=auth_headers())
    assert response.status_code == 200
    assert response.get_json()["result"] is True


def test_remove_like_not_found(client, seed_data):
    response = client.delete(f"/api/tweets/{seed_data['tweet2_id']}/likes", headers=auth_headers())
    assert response.status_code == 400


def test_upload_media_success(client):
    data = {"file": (BytesIO(b"fake image content"), "test.jpg")}
    response = client.post(
        "/api/medias",
        headers=auth_headers(),
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["result"] is True
    assert "media_id" in body


def test_upload_media_missing_file(client):
    response = client.post(
        "/api/medias",
        headers=auth_headers(),
        data={},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


def test_create_tweet_success(client):
    payload = {"tweet_data": "New tweet from test", "tweet_media_ids": []}
    response = client.post("/api/tweets", headers=auth_headers(), json=payload)
    assert response.status_code == 201
    assert response.get_json()["result"] is True


def test_create_tweet_missing_text(client):
    response = client.post("/api/tweets", headers=auth_headers(), json={})
    assert response.status_code == 400


def test_delete_tweet_success(client, seed_data):
    response = client.delete(f"/api/tweets/{seed_data['tweet1_id']}", headers=auth_headers())
    assert response.status_code == 200
    assert response.get_json()["result"] is True


def test_delete_tweet_not_owner(client, seed_data):
    response = client.delete(f"/api/tweets/{seed_data['tweet2_id']}", headers=auth_headers())
    assert response.status_code == 403


def test_delete_tweet_not_found(client):
    response = client.delete("/api/tweets/999999", headers=auth_headers())
    assert response.status_code == 404