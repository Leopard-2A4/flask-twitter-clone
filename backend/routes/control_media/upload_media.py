from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import models
from models import Media
from routes.general import require_api_key, error_response, log_error_in_file

@require_api_key
def upload_media():
    """
    Upload media
    ---
    tags:
      - Media
    security:
      - ApiKeyAuth: []
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        required: true
        type: file
    responses:
      201:
        description: Media uploaded
        schema:
          type: object
          properties:
            result:
              type: boolean
            media_id:
              type: integer
    """
    try:
        if 'file' not in request.files:
            return error_response("MISSING_FILE", "Файл не предоставлен", 400)

        file = request.files['file']

        if file.filename == '':
            return error_response("EMPTY_FILENAME", "Имя файла пустое", 400)

        upload_dir = current_app.config.get(
            "UPLOAD_FOLDER",
            os.path.join(current_app.root_path, "static", "uploads")
        )
        os.makedirs(upload_dir, exist_ok=True)

        safe_name = secure_filename(file.filename)
        filename = f"{request.user.id}_{safe_name}"
        abs_path = os.path.join(upload_dir, filename)

        file.save(abs_path)

        media = Media(file_path=f"/static/uploads/{filename}")
        models.db.session.add(media)
        models.db.session.commit()

        return jsonify({
            "result": True,
            "media_id": media.id
        }), 201

    except Exception as e:
        models.db.session.rollback()
        log_error_in_file(e)
        return error_response("UPLOAD_ERROR", str(e), 500)