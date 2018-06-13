from flask import Flask
from flask import request, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
app.logger.disabled = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/addnewmovie", methods=["GET", "PUT"])
def getmoviedetails:
    movie_id = int(request.args.get('movie_id', ''))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)