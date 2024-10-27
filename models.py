from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, UTC

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tags = db.Column(db.String(500), nullable=True)  # Поле для хранения тегов

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    likes = db.Column(db.Integer, default=0)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(UTC))
    username = db.Column(db.String(80), nullable=False)
    article_title = db.Column(db.String(200), nullable=False)
    action = db.Column(db.String(20), nullable=False)