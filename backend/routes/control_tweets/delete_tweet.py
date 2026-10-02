from flask import request, jsonify
import models
from models.tweets import Tweet
from routes.general import require_api_key, error_response, log_error_in_file


@require_api_key
def delete_tweet(tweet_id: int):
    """
    Delete tweet
    ---
    tags:
      - Tweets
    security:
      - ApiKeyAuth: []
    parameters:
      - name: tweet_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Tweet deleted
    """
    try:
        tweet = Tweet.query.filter_by(id=tweet_id).first()

        if not tweet:
            return error_response("TWEET_NOT_FOUND", "Твит не найден", 404)

        if tweet.author_id != request.user.id:
            return error_response("NOT_OWNER", "Вы можете удалять только свои твиты", 403)

        models.db.session.delete(tweet)
        models.db.session.commit()

        return jsonify({
            "result": True
        }), 200

    except Exception as e:
        models.db.session.rollback()
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)
