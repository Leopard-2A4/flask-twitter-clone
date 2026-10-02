from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.database import db
from datetime import datetime


class Tweet(db.Model):
    """
    Модель твита (сообщения микроблога).

    Attributes:
        id: Primary key
        content: Текст твита
        author_id: ID автора (ссылка на users)
        created_at: Дата создания
    """
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(1000), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    author = relationship('User', back_populates='tweets')
    media = relationship('Media', back_populates='tweet', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='tweet', cascade='all, delete-orphan')

    def get_popularity(self):
        """Возвращает количество лайков твита."""
        return len(self.likes)

    def __repr__(self):
        return f'<Tweet {self.id}: {self.content[:50]}>'