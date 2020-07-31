import zlib

import urllib3

import imdb.data


def get_genres(genres_string):
    if genres_string == "\\N":
        return None
    return genres_string.split(",")


def transform_line_to_movie(line):
    data = line.split("\t")
    if data[1] != "movie":
        return None
    return imdb.data.Movie(data[0], data[2], data[3], get_genres(data[8]), data[5])


def transform_line_to_rating(line):
    data = line.split("\t")
    return imdb.data.Rating(data[0], data[1], data[2])


def extract_genres(movies):
    s = set()
    for movie in movies:
        if movie.genres:
            for genre in movie.genres:
                s.add(genre)
    return s


def extract_data(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status != 200:
        return Exception("Could not get basic content from IMDb")

    data_bytes = zlib.decompress(response.data, 15 + 32)

    lines = data_bytes.decode("utf-8").split("\n")
    lines.pop(0)
    lines.pop()
    return lines


def add_rating_to_movie(movie, ratings):
    if ratings.get(movie.tconst):
        movie.add_rating(ratings.get(movie.tconst))


def filter_movie_under_threshold(movie, number_of_rates_threshold):
    if movie.number_of_votes is not None and int(movie.number_of_votes) >= number_of_rates_threshold:
        return movie


class Extractor:
    def __init__(self, configuration):
        self.configuration = configuration

    def extract_movies(self):
        lines = extract_data(self.configuration.basic_url)
        return list(filter(None, [transform_line_to_movie(line) for line in lines]))

    def add_ratings_to_movies(self, movies):
        lines = extract_data(self.configuration.ratings_url)
        ratings = {}
        for line in lines:
            rating = transform_line_to_rating(line)
            ratings[rating.tconst] = rating
        return [add_rating_to_movie(movie, ratings) for movie in movies]

    def get_movies_over_rate_threshold(self, movies):
        return list(filter(None,
                           [filter_movie_under_threshold(movie, self.configuration.number_of_ratings_threshold)
                            for movie in movies]))
