from model.database import db_session
from model.models import moviedetails
def add_new_movie(movie_id, movie_name, genre, price, popularity_index, run_length_in_minutes):
    db_session.add(moviedetails(movie_id, movie_name, genre, price, popularity_index, run_length_in_minutes))
    db_session.commit()
