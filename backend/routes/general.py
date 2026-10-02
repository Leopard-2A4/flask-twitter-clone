from pathlib import Path
from flask import request, jsonify
from models.users import User
from functools import wraps
from datetime import datetime
import traceback


def log_error_in_file(error):
    errors_dir = Path(__file__).parent / "errors_dir"
    errors_dir.mkdir(exist_ok=True, parents=True)

    today = datetime.today().strftime('%Y-%m-%d')
    file_path = errors_dir / f"{today}.txt"

    tb = traceback.format_exception(type(error), error, error.__traceback__)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}\n")
        f.write('\n'.join(tb))
        f.write('\n')

def get_user_by_api_key(api_key: str) -> User:
    return User.query.filter_by(name=api_key).first()

def require_api_key(f):
    """
    Декоратор для проверки api-key в запросе.

    Args:
        f: Функция, которую защищать

    Returns:
        wrapped: Защищённая функция
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('api-key')

        if not api_key:
            return jsonify({
                "result": False,
                "error_type": "MISSING_API_KEY",
                "error_message": "API ключ не предоставлен"
            }), 401

        user = get_user_by_api_key(api_key)

        if not user:
            return jsonify({
                "result": False,
                "error_type": "INVALID_API_KEY",
                "error_message": "Неверный API ключ"
            }), 401

        request.user = user

        return f(*args, **kwargs)

    return decorated


def error_response(error_type: str, error_message: str, status_code: int = 500):
    """
    Создает стандартный ответ об ошибке.

    Args:
        error_type: Тип ошибки
        error_message: Сообщение об ошибке
        status_code: HTTP статус код

    Returns:
        tuple: (JSON ответ, статус код)
    """
    return jsonify({
        "result": False,
        "error_type": error_type,
        "error_message": error_message
    }), status_code
