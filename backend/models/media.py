from models.database import db

class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"), nullable=True)

    tweet = db.relationship("Tweet", back_populates="media")

    def __repr__(self):
        return f"<Media {self.id}: {self.file_path}>"