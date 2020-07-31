def create_movie_uniqueness_constraint(tx):
    tx.run("CREATE CONSTRAINT movie_constraint ON (m:Movie) ASSERT m.id IS UNIQUE")


def create_genre_uniqueness_constraint(tx):
    tx.run("CREATE CONSTRAINT genre_constraint ON (g:Genre) ASSERT g.id IS UNIQUE")


def remove_movie_nodes(tx):
    tx.run("MATCH (n) DETACH DELETE n")


def add_genre_node(tx, genre):
    tx.run("CREATE (g:Genre {name: $name})", name=genre)


def add_movie_node(tx, movie):
    tx.run("CREATE (m:Movie {id: $id, name: $primary_title, original_title: $original_title, "
           "average_rating: $average_rating, number_of_votes: $number_of_votes, year: $year})",
           id=movie.tconst, primary_title=movie.primary_title, original_title=movie.original_title,
           average_rating=movie.average_rating, number_of_votes=movie.number_of_votes, year=movie.year)


def add_movie_to_genre_relationship(tx, tconst, genre):
    tx.run("MATCH (m:Movie),(g:Genre) WHERE m.id = $id AND g.name = $name CREATE (m)-[r:IN_GENRE]->(g)", id=tconst,
           name=genre)


def get_movies_based_on_genre_similarity(tx, chosen_movie):
    return tx.run("MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(n:Movie) "
                  "WHERE m.name = $chosen_movie "
                  "WITH n, COLLECT(g.name) AS genres, COUNT(*) AS commonGenres "
                  "RETURN n.name, n.original_title, genres, n.average_rating, n.number_of_votes, n.year "
                  "ORDER BY commonGenres, n.average_rating DESC LIMIT 30", chosen_movie=chosen_movie)


def get_all_users(tx):
    return tx.run("MATCH (u:User) RETURN u.name")


def create_user(tx, name):
    return tx.run("CREATE (u:User {name: $name}) RETURN u.name", name=name).single()[0]


def user_rate_movie(tx, username, movie_name, rating):
    return tx.run("MATCH (m:Movie),(u:User) "
                  "WHERE m.name = $movie_name AND u.name = $username "
                  "CREATE (u)-[r:RATED { rating: $rating}]->(m) "
                  "RETURN r.rating",
                  movie_name=movie_name, username=username, rating=rating).single()[0]


def get_ratings(tx, username):
    return tx.run("MATCH (u:User)-[r:RATED]->(m:Movie) "
                  "WHERE u.name = $username "
                  "RETURN m.name, r.rating, m.year", username=username)


def get_movies_based_on_user_history(tx, username):
    return tx.run("MATCH (u:User {name: $username})-[r:RATED]->(m:Movie), "
                  "(m)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(result:Movie) "
                  "WHERE NOT EXISTS( (u)-[:RATED]->(result)) "
                  "WITH result, [g.name, COUNT(*)] AS scores "
                  "RETURN result.name, result.year, REDUCE (s=0,x in COLLECT(scores) | s+x[1]) AS score "
                  "ORDER BY score DESC LIMIT 10", username=username)
