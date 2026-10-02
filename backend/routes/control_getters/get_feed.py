from flask import jsonify
from models import Tweet
from routes.general import require_api_key, error_response
from routes.general import log_error_in_file

@require_api_key
def get_feed():
    """
    Get feed
    ---
    tags:
      - Tweets
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Feed data
    """
    try:
        tweets = Tweet.query.order_by(Tweet.created_at.desc()).all()

        tweets_data = []

        for tweet in tweets:
            attachments = []
            for media in tweet.media:
                attachments.append(media.file_path)

            likes_data = []
            for like in tweet.likes:
                likes_data.append({
                    "user_id": like.user.id,
                    "name": like.user.name
                })

            tweets_data.append({
                "id": tweet.id,
                "content": tweet.content,
                "attachments": attachments,
                "author": {
                    "id": tweet.author.id,
                    "name": tweet.author.name
                },
                "likes": likes_data
            })

        return jsonify({
            "result": True,
            "tweets": tweets_data
        }), 200

    except Exception as e:
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)