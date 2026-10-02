from sqlalchemy import Column, Integer,ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from models.database import db


class Follow(db.Model):
    """Модель фолловинга."""
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    follower = relationship(
        'User',
        back_populates='following',
        foreign_keys='Follow.follower_id'
    )
    followed = relationship(
        'User',
        back_populates='followers',
        foreign_keys='Follow.followed_id'
    )

    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),
    )

    def __repr__(self):
        return f'<Follow {self.follower_id} -> {self.followed_id}>'