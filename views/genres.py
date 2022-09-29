from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Genre, GenreSchema


genre_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        return genres_schema.dump(Genre.query.all()), 200

    def post(self):
        data = request.json
        new_genre = Genre(**data)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        return genre_schema.dump(Genre.query.get(gid)), 200


    def put(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        data = request.json
        genre.name = data.get("name")

        db.session.add(genre)
        db.session.commit()
        return "", 204


    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        db.session.delete(genre)
        db.session.commit()
        return "", 204
