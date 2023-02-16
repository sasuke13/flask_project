from flask_restful import Resource
from marshmallow import ValidationError
from flask import request

from src.schemas.actors import ActorSchema
from src import app, db
from src.database.models import Actor


@app.route('/')
class ActorListApi(Resource):
    actor_schema = ActorSchema()

    def get(self, uuid=None):
        if not uuid:
            actors = db.session.query(Actor).all()
            return self.actor_schema.dump(actors, many=True)
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        return self.actor_schema.dump(actor), 200

    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201

    def put(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        try:
            actor = self.actor_schema.load(request.json, instance=actor, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return {'message': 'ok'}
        #return self.actor_schema.dump(actor), 200

    def patch(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        try:
            actor = self.actor_schema.load(request.json, instance=actor, partial=True, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        if actor.name or actor.birthday or actor.is_active:
            db.session.add(actor)
            db.session.commit()
            return self.actor_schema.dump(actor), 200
        else:
            return {'message': 'wrong data'}, 400

    def delete(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        db.session.delete(actor)
        db.session.commit()
        return '', 204
