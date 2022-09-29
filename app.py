from flask import Flask
from flask_restx import Api
from config import Config
from setup_db import db
from models import Movie, Director, Genre
from views.movies import movie_ns
from views.directors import director_ns
from views.genres import genre_ns
from data import data


data = data


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    create_data(app, db, data)


def create_data(app, db, data):
    with app.app_context():
        db.drop_all()
        db.create_all()
        for movie in data["movies"]:
            m = Movie(
                id=movie["pk"],
                title=movie["title"],
                description=movie["description"],
                trailer=movie["trailer"],
                year=movie["year"],
                rating=movie["rating"],
                genre_id=movie["genre_id"],
                director_id=movie["director_id"],
            )
            with db.session.begin():
                db.session.add(m)

        for director in data["directors"]:
            d = Director(
                id=director["pk"],
                name=director["name"],
            )
            with db.session.begin():
                db.session.add(d)

        for genre in data["genres"]:
            d = Genre(
                id=genre["pk"],
                name=genre["name"],
            )
            with db.session.begin():
                db.session.add(d)


app = create_app(Config())


if __name__ == '__main__':
    app.run(debug=True)
