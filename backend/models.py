from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255))
    author = db.Column(db.String(255))
    title = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    url = db.Column(db.String(2048), unique=True)
    urlToImage = db.Column(db.String(2048))
    publishedAt = db.Column(db.DateTime)
    cachedAt = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "urlToImage": self.urlToImage,
            "publishedAt": self.publishedAt.isoformat() if self.publishedAt else None,
            "cachedAt": self.cachedAt.isoformat() if self.cachedAt else None
        }
