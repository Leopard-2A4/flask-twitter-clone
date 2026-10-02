from flask import request, jsonify
import models
from models import User, Follow
from routes.general import require_api_key, error_response, log_error_in_file

@require_api_key
def follow_user(user_id: int):
    """
    Follow user
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
        description: ID пользователя, на которого подписываемся
    responses:
      201:
        description: Successfully followed user
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: true
      400:
        description: Already following or invalid request
        schema:
          type: object
          properties:
            result:
              type: boolean
              example: false
            error_type:
              type: string
            error_message:
              type: string
    """
    try:
        target_user = User.query.filter_by(id=user_id).first()

        if not target_user:
            return error_response("USER_NOT_FOUND", "Пользователь не найден", 404)

        if target_user.id == request.user.id:
            return error_response("CANNOT_FOLLOW_SELF", "Нельзя фолловить себя", 400)

        existing_follow = Follow.query.filter_by(
            follower_id=request.user.id,
            followed_id=target_user.id
        ).first()

        if existing_follow:
            return error_response("ALREADY_FOLLOWING", "Вы уже фолловите этого пользователя", 400)

        follow = Follow(follower_id=request.user.id, followed_id=target_user.id)
        models.db.session.add(follow)
        models.db.session.commit()

        return jsonify({
            "result": True
        }), 201

    except Exception as e:
        models.db.session.rollback()
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)