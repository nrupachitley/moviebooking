from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import DOUBLE
from model.database import Base

class moviedetails(Base):
    __tablename__ = 'moviedetails'
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String(200), unique=True)
    genre = Column(String(200), unique=True)
    price = Column(DOUBLE, unique=True)
    popularity_index = Column(Integer, unique=True)
    run_lengt_in_minutes = Column(Integer, unique=True)

    def __init__(self, movie_id, movie_name, genre, price, popularity_index, run_lengt_in_minutes):
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.genre = genre
        self.price = price
        self.popularity_index = popularity_index
        self.run_lengt_in_minutes = run_lengt_in_minutes