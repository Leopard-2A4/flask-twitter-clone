from flask import request, jsonify
import models
from models import Follow
from routes.general import require_api_key, error_response, log_error_in_file

@require_api_key
def unfollow_user(user_id: int):
    """
    Unfollow user
    ---
    tags:
      - Follow
    security:
      - ApiKeyAuth: []
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
        description: ID пользователя, от которого отписываемся
    responses:
      200:
        description: Successfully unfollowed user
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
      400:
        description: Not following user
        schema:
          type: object
          properties:
            result:
              type: boolean
            error_type:
              type: string
            error_message:
              type: string
    """
    try:
        follow = Follow.query.filter_by(
            follower_id=request.user.id,
            followed_id=user_id
        ).first()

        if not follow:
            return error_response("NOT_FOLLOWING", "Вы не фолловите этого пользователя", 400)

        models.db.session.delete(follow)
        models.db.session.commit()

        return jsonify({
            "result": True
        }), 200

    except Exception as e:
        models.db.session.rollback()
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)