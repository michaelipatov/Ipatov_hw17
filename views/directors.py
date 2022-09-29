from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Director, DirectorSchema


director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return directors_schema.dump(Director.query.all()), 200

    def post(self):
        data = request.json
        new_director = Director(**data)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        return director_schema.dump(Director.query.get(did)), 200


    def put(self, did: int):
        director = Director.query.get(did)
        if not director:
            return "", 404
        data = request.json
        director.name = data.get("name")

        db.session.add(director)
        db.session.commit()
        return "", 204


    def delete(self, did: int):
        director = Director.query.get(did)
        if not director:
            return "", 404
        db.session.delete(director)
        db.session.commit()
        return "", 204
