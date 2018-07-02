import handler
from handler import app

def add_new_movie(movie_id, movie_name, genre, price, run_time_in_minutes):
    d = handler.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO movie_details (movie_id,movie_name,genre,price,run_time_in_minutes) VALUES (%s,%s,%s,%s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query,
                       (movie_id, movie_name, genre, price, run_time_in_minutes))
        d.commit()
        # Commit your changes in the database
        print("inserted", movie_id, movie_name, genre, price, run_time_in_minutes)
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def add_movie_theater(movie_id, theater_number, screen_id, show_time_object, release_date_object, end_date_object):
    d = handler.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO movie_theater (movie_id, theater_number, screen_id, show_timing, release_date, end_date) VALUES (%s,%s,%s,%s,%s,%s)"
    try:
        # Execute the SQL command
        print(show_time_object.strftime('%T'))
        cursor.execute(query,
                       (movie_id, theater_number, screen_id, show_time_object.strftime('%H:%M:%S'),
                        release_date_object.strftime('%Y-%m-%d'), end_date_object.strftime('%Y-%m-%d')))
        d.commit()
        # Commit your changes in the database
        print("inserted", movie_id, theater_number, screen_id, show_time_object.strftime('%T'),
              release_date_object.strftime('%Y-%m-%d'), end_date_object.strftime('%Y-%m-%d'))
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def add_new_user(login_id, password):
    d = handler.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO user_details (login_id, password) VALUES (%s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query,(login_id, password))
        d.commit()
        # Commit your changes in the database
        print("inserted", login_id, password)
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


def get_theaters(email):
    try:
        d = handler.mysql.connect()
        cursor = d.cursor()
        query = "SELECT theater_number,theater_name FROM theaters WHERE company = %s"
        cursor.execute(query,(email))
        results = cursor.fetchall()
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        print e
        return "NOT OK"

def check_login(email):
    try:
        d = handler.mysql.connect()
        cursor = d.cursor()
        query = "SELECT login_id,password FROM user_details WHERE login_id = %s"
        cursor.execute(query, (email))
        results = cursor.fetchall()
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        print e
        return "NOT OK"


def get_movies(today_date):
    try:
        d = handler.mysql.connect()
        cursor = d.cursor()
        query = "SELECT movie_details.movie_name,movie_theater.movie_id,theaters.theater_name,theaters.theater_number,movie_theater.show_timing, movie_theater.screen_id,movie_theater.release_date,movie_theater.end_date" \
                " FROM movie_details JOIN movie_theater ON movie_details.movie_id=movie_theater.movie_id JOIN theaters ON movie_theater.theater_number=theaters.theater_number " \
                "WHERE movie_theater.release_date <= %s AND movie_theater.end_date >= %s"
        cursor.execute(query, (today_date, today_date))
        results = cursor.fetchall()
        ans = []
        results_list = list(results)
        for r in results_list:
            l = list(r)
            l[4] = str(l[4])
            l[6] = str(l[6])
            l[7] = str(l[7])
            r = tuple(l)
            ans.append(r)
        results = tuple(ans)
        # print (results)
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        print e
        return "NOT OK"

def get_max_seats(theater_number, screen_id):
    try:
        d = handler.mysql.connect()
        cursor = d.cursor()
        query = "SELECT max_row,max_col FROM seats WHERE theater_number = %s AND screen_id = %s"
        cursor.execute(query, (theater_number, screen_id))
        results = cursor.fetchall()
        # print(results)
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        print e
        return "NOT OK"

def hold_seats(login_id, theater_number, screen_id, seat_row, seat_col, show_date, show_timing, status):
    d = handler.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO seat_status (theater_number,screen_id,seat_row,seat_col,show_date,show_timing,status,login_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query,
                       (theater_number, screen_id, seat_row, seat_col, show_date, show_timing, status, login_id))
        d.commit()
        # Commit your changes in the database
        print("inserted", theater_number, screen_id, seat_row, seat_col, show_date, show_timing, status, login_id)
    except Exception as e:
        print(e)
        d.rollback()


def get_seat_status(theater_number, screen_id, time, today_date):
    try:
        d = handler.mysql.connect()
        cursor = d.cursor()
        query = "SELECT seat_row,seat_col FROM seat_status WHERE theater_number = %s AND screen_id = %s AND show_timing = %s AND show_date = %s"
        cursor.execute(query, (theater_number, screen_id, time, today_date))
        results = cursor.fetchall()
        # print(results)
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        print e
        return "NOT OK"

def get_movie_details(movie_id):
    try:
        d = handler.mysql.connect()
        cursor = d.cursor()
        query = "SELECT movie_name, price FROM movie_details WHERE movie_id = %s"
        cursor.execute(query, (movie_id))
        results = cursor.fetchall()
        # print(results)
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        print e
        return "NOT OK"


def change_seat_status(login_id, theater_number, screen_id, show_date, show_time):
    d = handler.mysql.connect()
    cursor = d.cursor()
    query = "UPDATE seat_status SET status= %s WHERE theater_number = %s AND screen_id = %s AND show_date = %s AND show_timing = %s AND login_id = %s"
    try:
        cursor.execute(query, ("Booked",theater_number, screen_id, show_date, show_time, login_id))
        d.commit()

    except Exception as e:
        print(e)
        d.rollback()

def booked(login_id, movie_id, theater_number, show_date, show_time, seat_row, seat_col, price):
    d = handler.mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO booked (login_id,movie_id,theater_number,show_date,show_time,seat_row,seat_col,price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query,
                       (login_id, movie_id, theater_number, show_date, show_time, seat_row, seat_col, price))
        d.commit()
        # Commit your changes in the database
        print("inserted", login_id, movie_id, theater_number, show_date, show_time, seat_row, seat_col, price)
    except Exception as e:
        print(e)
        d.rollback()


def delete_seat_status(login_id, theater_number, screen_id, show_date, show_time):
    d = handler.mysql.connect()
    cursor = d.cursor()
    query = "DELETE FROM seat_status WHERE login_id = %s AND theater_number = %s AND screen_id = %s AND show_date = %s AND show_timing = %s"
    try:
        cursor.execute(query, (login_id,theater_number, screen_id, show_date, show_time))
        d.commit()

    except Exception as e:
        print(e)
        d.rollback()