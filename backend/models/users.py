from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.database import db

class User(db.Model):
    """
    Модель пользователя сервиса микроблогов.

    Attributes:
        id: Primary key
        name: Имя пользователя (имя берется из api-key)
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    tweets = relationship('Tweet', back_populates='author', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='user', cascade='all, delete-orphan')
    followers = relationship(
        'Follow',
        back_populates='followed',
        foreign_keys='Follow.followed_id',
        cascade='all, delete-orphan'
    )
    following = relationship(
        'Follow',
        back_populates='follower',
        foreign_keys='Follow.follower_id',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'