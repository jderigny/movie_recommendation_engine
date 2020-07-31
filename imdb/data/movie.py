class Movie:
    def __init__(self, tconst, primary_title, original_title, genres, year):
        self.tconst = tconst
        self.primary_title = primary_title
        self.original_title = original_title
        self.genres = genres
        self.average_rating = None
        self.number_of_votes = None
        self.year = year

    def add_rating(self, rating):
        self.average_rating = rating.average_rating
        self.number_of_votes = rating.number_of_votes
