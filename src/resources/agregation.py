from flask_restful import Resource
from sqlalchemy import func

from src import db, app
from src.database.models import Film, Actor


@app.route('/')
class Aggregation(Resource):
    def get(self):
        max_length = db.session.query(func.max(Film.length)).scalar()
        min_length = db.session.query(func.min(Film.length)).scalar()
        counter = db.session.query(func.count(Film.id)).filter(Film.title.ilike("%deathly hallows%")).scalar()
        return {
            "max length": max_length,
            "min length": min_length,
            "count": counter,
            "actor count": actors
        }