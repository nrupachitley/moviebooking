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
        query = "SELECT movie_details.movie_name,theaters.theater_name,theaters.theater_number,movie_theater.show_timing, movie_theater.screen_id FROM movie_details " \
                "JOIN movie_theater ON movie_details.movie_id=movie_theater.movie_id JOIN theaters ON movie_theater.theater_number=theaters.theater_number " \
                "WHERE movie_theater.release_date <= %s AND movie_theater.end_date >= %s"
        cursor.execute(query, (today_date, today_date))
        results = cursor.fetchall()
        ans = []
        results_list = list(results)
        for r in results_list:
            l = list(r)
            l[4] = str(l[4])
            r = tuple(l)
            ans.append(r)
        results = tuple(ans)
        # print (results)
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        print e
        return "NOT OK"