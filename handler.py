from flask import Flask
from flask import request, render_template
from flask import jsonify
from controllers import control
from flaskext.mysql import MySQL

app = Flask(__name__)
app.logger.disabled = False

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.errorhandler(400)
def bad_request(error=None, s=''):
    s = error
    message = {
        'status': 400,
        'message': 'BAD REQUEST ' + request.url,
        'reason': s
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp

@app.route("/addnewmovie", methods=["GET", "PUT"])
def getmoviedetails():
    movie_id = int(request.args.get('movie_id', ''))
    movie_name = request.args.get('movie_name', '')
    genre = request.args.get('genre', '')
    price = float(request.args.get('price', ''))
    popularity_index = int(request.args.get('popularity_index', ''))
    run_length_in_minutes = int(request.args.get('run_length_in_minutes', ''))

    if not movie_id:
        return bad_request(movie_id)

    elif not movie_name:
        return bad_request(movie_name)

    elif not genre:
        return bad_request(genre)

    elif not price:
        return bad_request(price)

    elif not popularity_index:
        return bad_request(popularity_index)

    elif not run_length_in_minutes:
        return bad_request(run_length_in_minutes)

    control.add_new_movie(movie_id, movie_name, genre, price, popularity_index, run_length_in_minutes)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)