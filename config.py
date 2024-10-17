import os

class Config:
    SECRET_KEY = os.environ.get('12345678') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Указываем базу данных SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
