from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from src import app, db
from src.database.models import Film
#from src.resources.auth import token_required
from src.schemas.films import FilmSchema
from src.services.film_service import FilmService


@app.route('/')
class FilmListApi(Resource):
    film_schema = FilmSchema()

    def get(self, uuid=None):
        if not uuid:
            films = FilmService.fetch_all_films(db.session) .options(
                selectinload(Film.actors)
            ).all()
            return self.film_schema.dump(films, many=True), 200
        film = FilmService.fetch_all_films_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        return self.film_schema.dump(film), 200

    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

    def put(self, uuid):
        film =  FilmService.fetch_all_films_by_uuid(db.session, uuid)
        if not film:
            return "", 404
        try:
            film = self.film_schema.load(request.json, instance=film, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

    def patch(self, uuid):
        film = FilmService.fetch_all_films_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        try:
            film = self.film_schema.load(request.json, instance=film, session=db.session, partial=True)
        except ValidationError as e:
            return {'message': str(e)}, 400
        if film.title:
            db.session.add(film)
            db.session.commit()
            return self.film_schema.dump(film), 200
        elif film.release_date:
            db.session.add(film)
            db.session.commit()
            return self.film_schema.dump(film), 200
        else:
            return {'message': 'wrong data'}, 400

    def delete(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204