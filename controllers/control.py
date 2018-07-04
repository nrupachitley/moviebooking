from model import models
from threading import Thread
from datetime import datetime
from flask_mail import Message

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
                d[r[0]][r[2]] = []
                d[r[0]][r[2]].append({})
                for dict in d[r[0]][r[2]]:
                    dict['show_timing'] = []
                    dict['show_timing'].append(r[4])
                    dict['theater_id'] = r[3]
                    dict['screen_id'] = r[5]
                    dict['movie_id'] = r[1]
                    dict['release_date'] = r[6]
                    dict['end_date'] = r[7]
            else:
                if r[2] not in d[r[0]]:
                    d[r[0]][r[2]] = []
                    d[r[0]][r[2]].append({})
                    for dict in d[r[0]][r[2]]:
                        dict['show_timing'] = []
                        dict['show_timing'].append(r[4])
                        dict['theater_id'] = r[3]
                        dict['screen_id'] = r[5]
                        dict['movie_id'] = r[1]
                        dict['release_date'] = r[6]
                        dict['end_date'] = r[7]
                else:
                    flag = 0
                    for dict in d[r[0]][r[2]]:
                        if dict['screen_id'] == r[5]:
                            dict['show_timing'].append(r[4])
                            flag = 1
                    if flag == 0:
                        d[r[0]][r[2]].append({})
                        list_dict = d[r[0]][r[2]]
                        last_dict = list_dict[-1]
                        last_dict['show_timing'] = []
                        last_dict['show_timing'].append(r[4])
                        last_dict['theater_id'] = r[3]
                        last_dict['screen_id'] = r[5]
                        last_dict['movie_id'] = r[1]
                        last_dict['release_date'] = r[6]
                        last_dict['end_date'] = r[7]
        # print d
        return d,0


def check_login(email):
    return models.check_login(email)


def seat_status(theater_number, screen_id, time, today_date):
    result1 = models.get_max_seats(theater_number,screen_id)
    result2 = models.get_seat_status(theater_number, screen_id, time, today_date)
    final_list = []
    if len(result2) != 0:
        for r in result2:
            s = r[0] + str(r[1])
            final_list.append(s)
    return result1, final_list


def hold_seats(info, info_dict):
    info_string = ''.join(info_dict)
    d = info_string.split('/')
    login_id = d[0]
    theater_number = int(d[1])
    screen_id = d[2]
    show_timing = d[3]
    show_date = d[4]
    status = 'Hold'

    for seat in info:
        seat_list = seat.split('-')
        seat_row = chr(int(seat_list[0]) + 64)
        seat_col = int(seat_list[1])
        models.hold_seats(login_id, theater_number, screen_id, seat_row, seat_col, show_date, show_timing, status)

def get_movie_details(info, info_dict):
    info_string = ''.join(info_dict)
    other_list = info_string.split('/')
    movie_id = int(other_list[5])

    seat_list = []
    for seat in info:
        temp_list = seat.split('-')
        seat_row = chr(int(temp_list[0]) + 64)
        seat_col = str(temp_list[1])
        seat_list.append(seat_row + seat_col)

    return models.get_movie_details(movie_id), seat_list, other_list

def mesage(information_list, mail):
    login_id = information_list[1]
    date = information_list[6]
    time = information_list[5]
    movie_name = information_list[8]

    date_object = datetime.strptime(date, '%Y-%m-%d')
    show_date = date_object.strftime('%Y-%m-%d')

    time_object = datetime.strptime(time, '%H:%M:%S')
    show_time = time_object.strftime('%H:%M:%S')

    all_seats = information_list[0].split('-')
    seats = ','.join(map(str, all_seats))

    message = "Movie tickets for " + movie_name + " has been confirmed for " + show_date + " at " + show_time + ". Seats: " + seats + "."

    msg = Message(message, recipients=[login_id])
    mail.send(msg)

def confirm_booking(complete_info_list, mail):
    information = complete_info_list.split('/')
    login_id = information[1]
    movie_id = int(information[2])
    theater_number = int(information[3])
    screen_id = information[4]
    date = information[6]
    time = information[5]
    price = float(information[7])

    date_object = datetime.strptime(date, '%Y-%m-%d')
    show_date = date_object.strftime('%Y-%m-%d')

    time_object = datetime.strptime(time, '%H:%M:%S')
    show_time = time_object.strftime('%H:%M:%S')

    models.change_seat_status(login_id, theater_number, screen_id, show_date, show_time)

    all_seats = information[0].split('-')
    for seat in all_seats:
        seat_row = str(seat[0])
        seat_col = int(seat[1])
        models.booked(login_id, movie_id, theater_number, show_date, show_time, seat_row, seat_col, price)

    mesage(information, mail)

def delete_booking(complete_info_list):
    information = complete_info_list.split('/')
    login_id = information[1]
    theater_number = int(information[3])
    screen_id = information[4]
    date = information[6]
    time = information[5]

    date_object = datetime.strptime(date, '%Y-%m-%d')
    show_date = date_object.strftime('%Y-%m-%d')

    time_object = datetime.strptime(time, '%H:%M:%S')
    show_time = time_object.strftime('%H:%M:%S')

    models.delete_seat_status(login_id, theater_number, screen_id, show_date, show_time)

