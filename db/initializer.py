import neobolt.exceptions as exceptions

import db


class Initializer:
    def __init__(self, driver):
        self.driver = driver

    def init_constraints(self):
        with self.driver.session() as session:
            try:
                session.write_transaction(db.request.create_movie_uniqueness_constraint)
            except exceptions.ClientError:
                print("movie_constraint already exists")
            try:
                session.write_transaction(db.request.create_genre_uniqueness_constraint)
            except exceptions.ClientError:
                print("genre_constraint already exists")

    def remove_data(self):
        with self.driver.session() as session:
            session.write_transaction(db.request.remove_movie_nodes)

    def insert_genres(self, genres):
        for genre in genres:
            with self.driver.session() as session:
                session.write_transaction(db.request.add_genre_node, genre)

    def insert_movies(self, movies):
        for movie in movies:
            with self.driver.session() as session:
                session.write_transaction(db.request.add_movie_node, movie)

    def insert_movies_relationship(self, movies):
        for movie in movies:
            if movie.genres:
                for genre in movie.genres:
                    with self.driver.session() as session:
                        session.write_transaction(db.request.add_movie_to_genre_relationship, movie.tconst, genre)
