import db


def transform_record_to_movie(record):
    return db.data.Movie(record[0], record[1], get_genres(record[2]), record[3], record[4], record[5])


def get_genres(*genres):
    return list(set(genres[0]))


def search_based_on_genre(driver, chosen_movie):
    with driver.session() as session:
        result = session.write_transaction(db.request.get_movies_based_on_genre_similarity, chosen_movie)
        return [transform_record_to_movie(record) for record in result]
