from flask import request, jsonify
from routes.general import require_api_key, error_response, log_error_in_file

@require_api_key
def get_my_profile():
    """
    Get my profile
    ---
    tags:
      - Users
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: User profile
    """
    try:
        followers = []
        for follow in request.user.followers:
            followers.append({
                "id": follow.follower.id,
                "name": follow.follower.name
            })

        following = []
        for follow in request.user.following:
            following.append({
                "id": follow.followed.id,
                "name": follow.followed.name
            })

        return jsonify({
            "result": True,
            "user": {
                "id": request.user.id,
                "name": request.user.name,
                "followers": followers,
                "following": following
            }
        }), 200

    except Exception as e:
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)
