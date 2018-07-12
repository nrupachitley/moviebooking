from flask import Flask
from flask import jsonify
from flask import Response
from flask import request, render_template
from flaskext.mysql import MySQL
import controllers.control
from datetime import datetime, timedelta
from flask_mail import Mail
from celery import Celery
from utils import utils

app = Flask(__name__)
app.logger.disabled = False

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '16Jan91*'
app.config['MYSQL_DATABASE_DB'] = 'moviebooking'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = app.debug
app.config['MAIL_USERNAME'] = 'atare.personal@gmail.com'
app.config['MAIL_PASSWORD'] = 'Dearth123'
app.config['MAIL_DEFAULT_SENDER'] = 'atare.personal@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = app.testing
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['CELERY_ACCEPT_CONTENT'] = ['pickle']
mail.init_app(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(serializer='pickle')
def sendReminderEmail(msg):
    with app.app_context():
        mail.send(msg)


# @app.route("/try", methods=["GET"])
# def tryasf():
#     add_together.delay(3, 9)
#     return Response("OK")


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/signIn")
def signIn():
    return render_template('signIn.html')


@app.route("/signUp")
def signUp():
    return render_template('signUp.html')


@app.errorhandler(400)
def bad_request(s, error=None):
    message = {
        'status': 400,
        'message': 'BAD REQUEST ' + request.url,
        'reason': error,
        'parameter': s,
    }
    print message
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.errorhandler(404)
def not_found(s, error=None):
    message = {
        'status': 400,
        'message': 'BAD REQUEST ' + request.url,
        'reason': error,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route("/addmovie", methods=["GET", "POST"])
def add_new_movie():
    movie_id = int(request.form['movie_id'])
    movie_name = request.form['movie_name']
    genre = request.form['genre']
    price = float(request.form['price'])
    run_time_in_minutes = int(request.form['run_time_in_minutes'])
    theater_number = int(request.form['theater_number'])
    show_timing = request.form['show_timing']
    screen_id = request.form['screen_id']
    release_date = request.form['release_date']
    end_date = request.form['end_date']

    show_time_list = show_timing.split(',')
    show_time_object_list = []

    try:
        for time in show_time_list:
            time_object = (datetime.strptime(time, '%H:%M:%S'))
            show_time_object_list.append(time_object)
    except ValueError:
        return bad_request(time)

    try:
        release_date_object = (datetime.strptime(release_date, '%Y-%m-%d'))
    except ValueError:
        return bad_request(release_date)
    try:
        end_date_object = (datetime.strptime(end_date, '%Y-%m-%d'))
    except ValueError:
        return bad_request(end_date)

    if movie_id <= 0:
        return bad_request(movie_id)

    if len(movie_name) == 0:
        return bad_request(movie_name)

    if len(genre) == 0:
        return bad_request(genre)

    if price <= 0:
        return bad_request(price)

    if run_time_in_minutes <= 0:
        return bad_request(run_time_in_minutes)

    if theater_number <= 0:
        return bad_request(theater_number)

    if screen_id <= 0:
        return bad_request(screen_id)
    screen_id_list = screen_id.split(',')

    controllers.control.add_items(movie_id, movie_name, genre, price, run_time_in_minutes, theater_number,
                                  screen_id_list,
                                  show_time_object_list, release_date_object, end_date_object)

    return Response("OK", status=200)


@app.route("/adduser", methods=["GET", "POST"])
def add_new_user():
    login_id = request.form['login_id']
    password = request.form['password']

    if len(login_id) == 0:
        return bad_request(login_id)

    if len(password) == 0:
        return bad_request(password)

    controllers.control.add_new_user(login_id, password)
    data, flag = controllers.control.admin_control(login_id)
    if flag == 1:
        return render_template('addmovie.html', data_theater=data)
    else:
        return render_template('movielist.html', data_movie=data, login=login_id)


@app.route("/bookMovie", methods=["GET", "POST"])
def book_movie():
    theater_number = int(request.form['theater_number'])
    details = request.form['details']
    show_date = request.form.getlist('show_date')

    l = details.split('-')
    show_timing = l[0]
    screen_id = l[1]
    movie_id = l[2]
    login_id = l[3]

    time_object = datetime.strptime(show_timing, '%H:%M:%S')
    time = time_object.strftime('%H:%M:%S')

    for curr_date in show_date:
        if curr_date != "":
            show_date_object = datetime.strptime(curr_date, '%Y-%m-%d')
    date = show_date_object.strftime('%Y-%m-%d')
    # return jsonify(date)

    info_dict = []
    info_dict.append(login_id)
    info_dict.append(theater_number)
    info_dict.append(screen_id)
    info_dict.append(time)
    info_dict.append(date)
    info_dict.append(movie_id)

    result1, result2 = controllers.control.seat_status(theater_number, screen_id, time, date)

    if result2 == 0:
        return render_template('movie_hall.html', hall_dim=result1, info_dict=info_dict)
    else:
        d = {65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H', 73: 'I', 74: 'J', 75: 'K', 76: 'L',
             77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T', 85: 'U', 86: 'V', 87: 'W', 88: 'X',
             89: 'Y', 90: 'Z'}
        return render_template('movie_hall_updated.html', hall_dim=result1, seat_update=result2, info_dict=info_dict,
                               letter_dict=d)


@app.route("/holdSeats", methods=["GET", "POST"])
def hold_seats():
    info = request.form.getlist('info')  # seat number reserved
    info_dict = request.form.getlist('info_dict')

    controllers.control.hold_seats(info, info_dict)
    result, seat_list, other_list = controllers.control.get_movie_details(info, info_dict)

    return render_template('payment.html', seat_info=seat_list, other_info=other_list, movie_info=result)


@app.route("/confirmBooking", methods=["POST"])
def confirm_booking():
    decision = request.form['decision']
    complete_info_list = request.form['complete_info_list']

    if decision == "Yes":
        controllers.control.confirm_booking(complete_info_list, mail)
        msg, show_date, show_time = controllers.control.reminerEmail(complete_info_list)
        time_obj = datetime.strptime(show_time, '%H:%M:%S') - timedelta(hours=1)
        utc_time = utils.convert_timezone(show_date, time_obj.time())
        sendReminderEmail.apply_async(args=(msg,), eta=utc_time)
        message = 'Booking Confirmed'
        return jsonify(message)
    else:
        controllers.control.delete_booking(complete_info_list)
        message = 'Booking Cancelled'
        return jsonify(message)


@app.route("/signin", methods=["GET", "POST"])
def login():
    login_id = request.form['login_id']
    password = request.form['password']

    if len(login_id) == 0:
        return bad_request(login_id)

    if len(password) == 0:
        return bad_request(password)

    result = controllers.control.check_login(login_id)

    if login_id == result[0][0] and password == result[0][1]:
        data, flag = controllers.control.admin_control(login_id)
        if flag == 1:
            return render_template('addmovie.html', data_theater=data)
        else:
            return render_template('movielist.html', data_movie=data, login=login_id)
    else:
        error = 'Invalid Login ID or password'
        return render_template('signIn.html', error=error)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
