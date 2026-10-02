from flask import Flask
from routes.control_tweets.create_tweet import create_tweet
from routes.control_tweets.delete_tweet import delete_tweet

from routes.control_media.upload_media import upload_media

from routes.control_likes.add_like import add_like
from routes.control_likes.remove_like import remove_like

from routes.control_follow.follow_user import follow_user
from routes.control_follow.unfollow_user import unfollow_user

from routes.control_getters.get_feed import get_feed
from routes.control_getters.get_my_profile import get_my_profile
from routes.control_getters.get_user_profile import get_user_profile

def init_routes(app: Flask):
    """
    Инициализирует все endpoint для Flask приложения.

    Args:
        app: Flask приложение
    """
    app.add_url_rule('/api/tweets', 'create_tweet', create_tweet, methods=['POST'])
    app.add_url_rule('/api/medias', 'upload_media', upload_media, methods=['POST'])
    app.add_url_rule('/api/tweets/<int:tweet_id>', 'delete_tweet', delete_tweet, methods=['DELETE'])
    app.add_url_rule('/api/tweets/<int:tweet_id>/likes', 'add_like', add_like, methods=['POST'])
    app.add_url_rule('/api/tweets/<int:tweet_id>/likes', 'remove_like', remove_like, methods=['DELETE'])
    app.add_url_rule('/api/users/<int:user_id>/follow', 'follow_user', follow_user, methods=['POST'])
    app.add_url_rule('/api/users/<int:user_id>/follow', 'unfollow_user', unfollow_user, methods=['DELETE'])
    app.add_url_rule('/api/tweets', 'get_feed', get_feed, methods=['GET'])
    app.add_url_rule('/api/users/me', 'get_my_profile', get_my_profile, methods=['GET'])
    app.add_url_rule('/api/users/<int:user_id>', 'get_user_profile', get_user_profile, methods=['GET'])