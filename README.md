# Twitter Clone API

REST API сервис, реализующий базовый функционал социальной сети:
создание твитов, лайки, подписки, работа с пользователями и медиа.

Проект построен на Flask + SQLAlchemy и развёрнут через Docker с nginx и frontend-приложением.

---

# Стек технологий

## Backend
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Flasgger (Swagger UI)
- pytest
- psycopg2

## Infrastructure
- Docker / Docker Compose
- Nginx

## Frontend
- Static SPA (собранные CSS/JS файлы)

---

# Архитектура проекта


backend/
models/ - ORM модели (User, Tweet, Like, Follow, Media)
routes/ - бизнес-логика API
control_* - разделённые контроллеры по доменам
static/uploads - загруженные медиафайлы
configuration.py - конфигурация Flask приложения
start.py - регистрация всех роутов
run.py - точка входа
conftest.py - фикстуры pytest
test_api.py - интеграционные тесты

frontend/
css/ - стили приложения
js/ - клиентская логика
index.html - точка входа frontend

nginx/
default.conf - reverse proxy конфигурация

---
# Структура проекта:
backend/
    models/
        __init__.py
        database.py
        follows.py
        likes.py
        media.py
        tweets.py
        users.py
    routes/
        control_follow/
            __init__.py
            follow_user.py
            unfollow_user.py
        control_getters/
            __init__.py
            get_feed.py
            get_my_profile.py
            get_user_profile.py
        control_likes/
            __init__.py
            add_like.py
            remove_like.py
        control_media/
            __init__.py
            upload_media.py
        control_tweets/
            __init__.py
            create_tweet.py
            delete_tweet.py
        errors_dir(директория которая отлавливает
                    записывает ошибки в файл)
        __init__.py
        general.py
        start.py
    static/
        uploads
    __init__.py
    configuration.py
    conftest.py
    create_test_data.py
    Dockerfile
    requirements.txt
    run.py
    test_api.py

frontend/
    css/
        app.45d81840.css
        chunk-6f77c742.8d9a3d9c.css
        chunk-10e0d5b4.130d80ef.css
        chunk-0420bcc4.d6bc3184.css
        chunk-732a3e8c.6334cd6b.css
        chunk-vendors.de691de6.css
    js/
        app.ee2cdef2.js
        app.ee2cdef2.js.map
        chunk-6f77c742.f09861a7.js
        chunk-6f77c742.f09861a7.js.map
        chunk-10e0d5b4.e80e67b6.js
        chunk-10e0d5b4.e80e67b6.js.map
        chunk-0420bcc4.11441662.js
        chunk-0420bcc4.11441662.js.map
        chunk-732a3e8c.57e36fb4.js
        chunk-732a3e8c.57e36fb4.js.map
        chunk-76301fe8.cc56c3b1.js
        chunk-76301fe8.cc56c3b1.js.map
        chunk-vendors.398321e0.js
        chunk-vendors.398321e0.js.map
    Dockerfile
    favicon.ico
    index.html
nginx/
    default.conf
.gitignore
docker-compose.yaml
README.md
---

# Запуск проекта

## Через Docker

```bash
docker-compose up --build
```
Или второй вариант:
```bash
docker-compose build --no-cache
```
```bash
docker-compose up -d
```
После запуска:

Frontend:
http://localhost/
Backend API (через nginx):
http://localhost/api/
Swagger документация:
http://localhost/apidocs/
Swagger API Documentation

Проект использует Flasgger для генерации Swagger UI.

Доступ:

/apidocs

Спецификация:

/apispec.json
Основные API эндпоинты
Твиты
Создание твита
POST /api/tweets
Удаление твита
DELETE /api/tweets/{tweet_id}
Получение ленты
GET /api/tweets
Лайки
Поставить лайк
POST /api/tweets/{tweet_id}/likes
Убрать лайк
DELETE /api/tweets/{tweet_id}/likes
Подписки
Подписаться на пользователя
POST /api/users/{user_id}/follow
Отписаться от пользователя
DELETE /api/users/{user_id}/follow
Пользователи
Мой профиль
GET /api/users/me
Профиль пользователя
GET /api/users/{user_id}
Медиа
Загрузка файла
POST /api/medias
Аутентификация

Во всех защищённых запросах используется API ключ.

Передаётся в headers:

api-key: <your_key>
База данных

Используется PostgreSQL.

При запуске через Docker:

База создаётся автоматически
таблицы создаются через SQLAlchemy (db.create_all())
Тестирование

Запуск тестов:
```bash
docker-compose up --build
```

Фикстуры находятся в conftest.py и используют SQLite in-memory.