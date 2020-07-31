import db
import recommendation


def transform_record_to_movie(record):
    return recommendation.data.Recommendation(record[0], record[1], record[2])


def search_based_on_user(driver, username):
    with driver.session() as session:
        result = session.write_transaction(db.request.get_movies_based_on_user_history, username)
        return [transform_record_to_movie(record) for record in result]
