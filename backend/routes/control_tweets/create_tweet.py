from flask import request, jsonify
import models
from models import Tweet, Media
from routes.general import require_api_key, error_response, log_error_in_file


@require_api_key
def create_tweet():
    """
    Create tweet
    ---
    tags:
      - Tweets
    security:
      - ApiKeyAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - tweet_data
          properties:
            tweet_data:
              type: string
              example: "Hello world"
            tweet_media_ids:
              type: array
              items:
                type: integer
    responses:
      201:
        description: Tweet created
        schema:
          type: object
          properties:
            result:
              type: boolean
            tweet_id:
              type: integer
    """
    try:
        data = request.get_json()

        if not data or 'tweet_data' not in data:
            return error_response("MISSING_TWEET_DATA", "Текст твита не предоставлен", 400)

        content = data['tweet_data']
        media_ids = data.get('tweet_media_ids', [])

        tweet = Tweet(
            content=content,
            author_id=request.user.id
        )

        models.db.session.add(tweet)
        models.db.session.commit()

        for media_id in media_ids:
            media = Media.query.filter_by(id=media_id).first()
            if media:
                media.tweet_id = tweet.id
                models.db.session.add(media)

        models.db.session.commit()

        return jsonify({
            "result": True,
            "tweet_id": tweet.id
        }), 201

    except Exception as e:
        models.db.session.rollback()
        log_error_in_file(e)
        return error_response("DB_ERROR", str(e), 500)
