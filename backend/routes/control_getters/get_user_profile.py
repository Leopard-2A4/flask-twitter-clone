from flask import request, jsonify
from models import User
from routes.general import error_response, get_user_by_api_key, log_error_in_file

def get_user_profile(user_id: int):
    """
    Get user profile
    ---
    tags:
      - Users
    security:
      - ApiKeyAuth: []
    parameters:
      - name: user_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: User profile
    """
    try:
        api_key = request.headers.get('api-key')

        if not api_key:
            return error_response("MISSING_API_KEY", "API ключ не предоставлен", 401)

        user = get_user_by_api_key(api_key)

        if not user:
            return error_response("INVALID_API_KEY", "Неверный API ключ", 401)

        target_user = User.query.filter_by(id=user_id).first()

        if not target_user:
            return error_response("USER_NOT_FOUND", "Пользователь не найден", 404)

        followers = []
        for follow in target_user.followers:
            followers.append({
                "id": follow.follower.id,
                "name": follow.follower.name
            })

        following = []
        for follow in target_user.following:
            following.append({
                "id": follow.followed.id,
                "name": follow.followed.name
            })

        return jsonify({
            "result": True,
            "user": {
                "id": target_user.id,
                "name": target_user.name,
                "followers": followers,
                "following": following
            }
        }), 200

    except Exception as e:
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)