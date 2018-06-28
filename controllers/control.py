from model import models
from threading import Thread
from datetime import datetime

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

    def __init__(self, movie_id, theater_number, screen_id_list, show_time_object_list, release_date_object, end_date_object):
        Thread.__init__(self)
        self.movie_id = movie_id
        self.theater_number = theater_number
        self.screen_id_list = screen_id_list
        self.show_time_object_list = show_time_object_list
        self.release_date_object = release_date_object
        self.end_date_object = end_date_object

    def run(self):
        for i in range(0, len(self.screen_id_list)):
            models.add_movie_theater(self.movie_id, self.theater_number, self.screen_id_list[i], self.show_time_object_list[i],
                                 self.release_date_object, self.end_date_object)


def add_items(movie_id, movie_name, genre, price, run_time_in_minutes, theater_number, screen_id_list, show_time_object_list,
              release_date_object, end_date_object):
    myCaller1 = Caller1(movie_id, movie_name, genre, price, run_time_in_minutes)
    myCaller1.start()
    myCaller2 = Caller2(movie_id, theater_number, screen_id_list, show_time_object_list, release_date_object, end_date_object)
    myCaller2.start()


def add_new_user(login_id, password):
    models.add_new_user(login_id, password)


def admin_control(login_id):
    email_add = login_id.split("@")
    email = email_add[1].split(".")
    if email[0] == "amc" or email[0] == "bc" or email[0] == "century":
        return models.get_theaters(email[0]),1
    else:
        today_date = datetime.today().strftime('%Y-%m-%d')
        result = models.get_movies(today_date)
        d = {}
        for r in result:
            if r[0] not in d:
                # print(r[0])
                d[r[0]] = {}
                # if r[1] not in d[r[0]]:
                d[r[0]][r[1]] = []
                d[r[0]][r[1]].append({})
                for dict in d[r[0]][r[1]]:
                    dict['show_timing'] = []
                    dict['show_timing'].append(r[3])
                    dict['theater_id'] = r[2]
                    dict['screen_id'] = r[4]
            else:
                if r[1] not in d[r[0]]:
                    d[r[0]][r[1]] = []
                    d[r[0]][r[1]].append({})
                    for dict in d[r[0]][r[1]]:
                        dict['show_timing'] = []
                        dict['show_timing'].append(r[3])
                        dict['theater_id'] = r[2]
                        dict['screen_id'] = r[4]
                else:
                    flag = 0
                    for dict in d[r[0]][r[1]]:
                        if dict['screen_id'] == r[4]:
                            dict['show_timing'].append(r[3])
                            flag = 1
                    if flag == 0:
                        d[r[0]][r[1]].append({})
                        list_dict = d[r[0]][r[1]]
                        last_dict = list_dict[-1]
                        last_dict['show_timing'] = []
                        last_dict['show_timing'].append(r[3])
                        last_dict['theater_id'] = r[2]
                        last_dict['screen_id'] = r[4]
        print d
        return d,0


def check_login(email):
    return models.check_login(email)