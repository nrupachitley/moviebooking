from model import models
from threading import Thread

class Caller1(Thread):

    def __init__(self, movie_id, movie_name, genre, price, run_time_in_minutes):
        Thread.__init__(self)
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.genre = genre
        self.price = price
        self.run_time_in_minutes = run_time_in_minutes

    def run(self):
        models.add_new_movie(self.movie_id, self.movie_name, self.genre, self.price, self.run_time_in_minutes)


class Caller2(Thread):

    def __init__(self, movie_id, theater_number, screen_id, show_time_object, release_date_object, end_date_object):
        Thread.__init__(self)
        self.movie_id = movie_id
        self.theater_number = theater_number
        self.screen_id = screen_id
        self.show_time_object = show_time_object
        self.release_date_object = release_date_object
        self.end_date_object = end_date_object

    def run(self):
        models.add_movie_theater(self.movie_id, self.theater_number, self.screen_id, self.show_time_object,
                                 self.release_date_object, self.end_date_object)


def add_items(movie_id, movie_name, genre, price, run_time_in_minutes, theater_number, screen_id, show_time_object,
              release_date_object, end_date_object):
    myCaller1 = Caller1(movie_id, movie_name, genre, price, run_time_in_minutes)
    myCaller1.start()
    myCaller2 = Caller2(movie_id, theater_number, screen_id, show_time_object, release_date_object, end_date_object)
    myCaller2.start()


def add_new_user(login_id, password):
    models.add_new_user(login_id, password)


def admin_control(login_id):
    print (login_id)
    email_add = login_id.split("@")
    email = email_add[1].split(".")
    # TODO: non admin users
    if email[0] == "amc" or email[0] == "bc" or email[0] == "century":
        return models.get_theaters(email[0]),1


def check_login(email):
    return models.check_login(email)