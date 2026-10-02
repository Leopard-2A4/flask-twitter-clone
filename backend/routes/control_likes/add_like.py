from flask import request, jsonify
import models
from models import Like, Tweet
from routes.general import require_api_key, error_response, log_error_in_file

@require_api_key
def add_like(tweet_id: int):
    """
    Add like
    ---
    tags:
      - Likes
    security:
      - ApiKeyAuth: []
    parameters:
      - name: tweet_id
        in: path
        required: true
        type: integer
    responses:
      201:
        description: Like added
    """
    try:
        tweet = Tweet.query.filter_by(id=tweet_id).first()

        if not tweet:
            return error_response("TWEET_NOT_FOUND", "Твит не найден", 404)

        existing_like = Like.query.filter_by(
            user_id=request.user.id,
            tweet_id=tweet_id
        ).first()

        if existing_like:
            return error_response("ALREADY_LIKED", "Вы уже лайкнули этот твит", 400)

        like = Like(user_id=request.user.id, tweet_id=tweet_id)
        models.db.session.add(like)
        models.db.session.commit()

        return jsonify({
            "result": True
        }), 201

    except Exception as e:
        models.db.session.rollback()
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)