from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Movie, MovieSchema


movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        query = Movie.query
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id and genre_id:
            query = query.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)
        elif director_id:
            query = query.filter(Movie.director_id == director_id)
        elif genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        return movies_schema.dump(query.all()), 200

    def post(self):
        data = request.json
        new_movie = Movie(**data)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        return movie_schema.dump(Movie.query.get(mid)), 200


    def put(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        data = request.json
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")

        db.session.add(movie)
        db.session.commit()
        return "", 204


    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204
