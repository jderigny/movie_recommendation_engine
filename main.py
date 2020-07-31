import datetime

import db
import imdb
import recommendation
import user


def initialize(driver):
    print("start database initialization")
    extractor = imdb.Extractor(imdb.Configure())
    start = datetime.datetime.now().timestamp()
    movies = extractor.extract_movies()
    print("{} movies extracted from IMDb website in {} s"
          .format(len(movies), datetime.datetime.now().timestamp() - start))
    start = datetime.datetime.now().timestamp()
    genres = imdb.extractor.extract_genres(movies)
    print("{} genres extracted from the movies in {} s"
          .format(len(genres), datetime.datetime.now().timestamp() - start))
    start = datetime.datetime.now().timestamp()
    extractor.add_ratings_to_movies(movies)
    print("ratings added from the IMDb website in {} s".format(datetime.datetime.now().timestamp() - start))
    start = datetime.datetime.now().timestamp()
    movies = extractor.get_movies_over_rate_threshold(movies)
    print("less rated movies removed in {} s, now {} movies to be inserted"
          .format(datetime.datetime.now().timestamp() - start, len(movies)))

    initializer = db.Initializer(driver)
    start = datetime.datetime.now().timestamp()
    initializer.remove_data()
    print("data removed in {} s".format(datetime.datetime.now().timestamp() - start))
    start = datetime.datetime.now().timestamp()
    initializer.init_constraints()
    print("constraints added in {} s".format(datetime.datetime.now().timestamp() - start))
    start = datetime.datetime.now().timestamp()
    initializer.insert_genres(genres)
    print("genres inserted into db in {} s".format(datetime.datetime.now().timestamp() - start))
    start = datetime.datetime.now().timestamp()
    initializer.insert_movies(movies)
    print("movies inserted into db in {} s".format(datetime.datetime.now().timestamp() - start))
    start = datetime.datetime.now().timestamp()
    initializer.insert_movies_relationship(movies)
    print("relationships inserted into db in {} s".format(datetime.datetime.now().timestamp() - start))
    username = "user_test"
    user.create_user(driver, username)
    user_connection = user.Connection(driver, username)
    user_connection.grade_movie("Inception", 9)
    user_connection.grade_movie("Titanic", 8)
    user_connection.grade_movie("Star Wars: Episode IV - A New Hope", 9)
    print("database initialized")


def recommend_by_genre(driver):
    print("enter movie name")
    result = recommendation.genre.search_based_on_genre(driver, input())
    for movie in result:
        print("name: '{}', original_name: '{}', year: {}, genres: '{}', average_rating: {}, number_of_votes: {}"
              .format(movie.name, movie.original_title, movie.year, movie.genres, movie.average_rating,
                      movie.number_of_votes))


def get_all_users(driver):
    print("retrieving all users")
    result = user.get_all_users(driver)
    for record in result:
        print("name: '{}'".format(record.name))
    print("retrieved all users")


def create_user(driver):
    print("enter a username for the new user")
    print("created : {}".format(user.create_user(driver, input())))


def connect_to_user(driver):
    print("enter a username to connect to the account")
    username = input()
    user_connection = user.Connection(driver, username)
    ratings = user_connection.get_ratings()
    [print("movie: '{}', year: {}, rating: {}".format(rating.name, rating.year, rating.rating)) for rating in ratings]
    print("enter a movie to rate")
    movie_name = input()
    print("enter a rating")
    rating = input()
    print(user_connection.grade_movie(movie_name, rating))
    print("movie rated")
    result = recommendation.user.search_based_on_user(driver, username)
    [print("movie: '{}', year: {}, score: {}".format(record.name, record.year, record.score)) for record in result]


if __name__ == "__main__":
    connection = db.Connect(db.Configure())

    print("enter 'init' to initialize the database or else press any key")
    if input() == "init":
        initialize(connection.driver)
    else:
        while True:
            print("press '1' to get recommendation by genre")
            print("press '2' to get all users")
            print("press '3' to create a user")
            print("press '4' to connect to a user")
            user_input = input()
            if user_input == "1":
                recommend_by_genre(connection.driver)
            elif user_input == "2":
                get_all_users(connection.driver)
            elif user_input == "3":
                create_user(connection.driver)
            elif user_input == "4":
                connect_to_user(connection.driver)
            elif user_input == "exit":
                break
            else:
                print("unrecognized entry")
            print()

    connection.close()
    print("program terminated")
