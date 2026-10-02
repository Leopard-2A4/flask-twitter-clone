from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models.database import db

class Like(db.Model):
    """
    Модель лайка (отношение пользователя к твиту).

    Attributes:
        id: Primary key
        user_id: ID пользователя (ссылка на users)
        tweet_id: ID твита (ссылка на tweets)
    """
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='likes')
    tweet = relationship('Tweet', back_populates='likes')

    __table_args__ = (
        UniqueConstraint('user_id', 'tweet_id'),
    )

    def __repr__(self):
        return f'<Like user={self.user_id} tweet={self.tweet_id}>'