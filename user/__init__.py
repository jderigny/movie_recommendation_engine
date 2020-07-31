import db


def transform_record_to_user(record):
    return db.data.User(record[0])


def transform_record_to_movie(record):
    return db.data.Rating(record[0], record[1], record[2])


def get_all_users(driver):
    with driver.session() as session:
        result = session.write_transaction(db.request.get_all_users)
        return [transform_record_to_user(record) for record in result]


def create_user(driver, username):
    with driver.session() as session:
        return session.write_transaction(db.request.create_user, username)


class Connection:
    def __init__(self, driver, username):
        self.driver = driver
        self.username = username

    def grade_movie(self, movie_name, rating):
        with self.driver.session() as session:
            return session.write_transaction(db.request.user_rate_movie, self.username, movie_name, rating)

    def get_ratings(self):
        with self.driver.session() as session:
            result = session.write_transaction(db.request.get_ratings, self.username)
            return [transform_record_to_movie(record) for record in result]
