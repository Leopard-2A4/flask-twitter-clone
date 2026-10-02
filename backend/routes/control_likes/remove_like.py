from flask import request, jsonify
import models
from models import Like
from routes.general import require_api_key, error_response, log_error_in_file

@require_api_key
def remove_like(tweet_id: int):
    """
    Remove like
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
      200:
        description: Like removed
    """
    try:
        like = Like.query.filter_by(
            user_id=request.user.id,
            tweet_id=tweet_id
        ).first()

        if not like:
            return error_response("LIKE_NOT_FOUND", "Вы не лайнули этот твит", 400)

        models.db.session.delete(like)
        models.db.session.commit()

        return jsonify({
            "result": True
        }), 200

    except Exception as e:
        models.db.session.rollback()
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)