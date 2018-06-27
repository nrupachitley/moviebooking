from flask import Flask, redirect, flash
from flask import jsonify
from flask import Response
from flask import request, render_template
from flaskext.mysql import MySQL
import controllers.control
from datetime import datetime
import model.models

app = Flask(__name__)
app.logger.disabled = False

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '16Jan91*'
app.config['MYSQL_DATABASE_DB'] = 'moviebooking'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@app.route("/try", methods=["GET", "POST"])
def temp():
    login_id = request.args.get('l', '')
    data, flag = controllers.control.admin_control(login_id)
    return render_template('movielist.html', data_movie=data)
    # t = controllers.control.admin_control()
    # return jsonify(t)

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
        'parameter': s,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route("/addmovie", methods=["GET", "POST"])
def add_new_movie():
    if request.form is not None and len(request.form) != 0:
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
    else:
        movie_id = int(request.args.get('movie_id', ''))
        movie_name = request.args.get('movie_name', '')
        genre = request.args.get('genre', '')
        price = float(request.args.get('price', ''))
        run_time_in_minutes = int(request.args.get('run_time_in_minutes', ''))
        theater_number = int(request.args.get('theater_number', ''))
        screen_id = request.args.get('screen_id', '')
        show_timing = request.args.get('show_timing', '')
        release_date = request.args.get('release_date', '')
        end_date = request.args.get('end_date', '')


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

    controllers.control.add_items(movie_id, movie_name, genre, price, run_time_in_minutes, theater_number, screen_id_list,
                                  show_time_object_list, release_date_object, end_date_object)

    return Response("OK", status=200)


@app.route("/adduser", methods=["GET", "POST"])
def add_new_user():
    if request.form is not None and len(request.form) != 0:
        login_id = request.form['login_id']
        password = request.form['password']
    else:
        login_id = request.args.get('login_id', '')
        password = request.args.get('password', '')

    if len(login_id) == 0:
        return bad_request(login_id)

    if len(password) == 0:
        return bad_request(password)

    controllers.control.add_new_user(login_id, password)
    data, flag = controllers.control.admin_control(login_id)
    if flag == 1:
        return render_template('addmovie.html', data_theater=data)
    else:
        return render_template('movielist.html', data_movie=data)


@app.route("/bookMovie", methods=["GET", "POST"])
def book_movie():
    print(request.form)
    if request.form is not None and len(request.form) != 0:
        theater_name = request.form['theater_name']
        show_timings = request.form['show_timings']
    else:
        theater_name = request.args.get('theater_name', '')
        show_timings = request.args.get('screen_time', '')
    return jsonify({
        'theater':theater_name,
        'show_timings':show_timings
    })


@app.route("/signin", methods=["GET", "POST"])
def login():
    if request.form is not None and len(request.form) != 0:
        login_id = request.form['login_id']
        password = request.form['password']
    else:
        login_id = request.args.get('login_id', '')
        password = request.args.get('password', '')

    if len(login_id) == 0:
        return bad_request(login_id)

    if len(password) == 0:
        return bad_request(password)

    result = controllers.control.check_login(login_id)

    # error = None
    if login_id == result[0][0] and password == result[0][1]:
        data, flag = controllers.control.admin_control(login_id)
        if flag == 1:
            return render_template('addmovie.html', data_theater=data)
        else:
            return render_template('movielist.html', data_movie=data)
    else:
        error = 'Invalid Login ID or password'
        return render_template('signIn.html', error=error)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)



