import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or'sqlite:///' + str(BASE_DIR / "data" / "flask_tutorial.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'you-will-never-know'
