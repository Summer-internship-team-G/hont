from flask import Flask, render_template, session, redirect, jsonify
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b"'`D\x96\xf3m\xeb\x01b\x11\xb5\x05\x14S\x96\xbd"

# Database
client = pymongo.MongoClient('mongodb://admin:password@localhost/mongodb')
db = client.webapp
# users_col = db['users']
# exercises_col = db['exercises']

# users_col.insert_one({"name": "zoommate_name", "id": "zoommate_id", "password": "zoommate_pw"})

# seoul_now = datetime.datetime.now()
# exercise = {"id": "zoommate_id", "exerDate": seoul_now.strftime("%Y-%m-%d"), "squartNum": 0, "pushupNum": 0, "exerTime": 0}
# exercises_col.insert_one(exercise)


# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return jsonify({ "error": "true" }), 400
  
  return wrap

@app.route('/checkLogin')
@login_required
def LoggedIn():
  return jsonify({ "error": "false" }), 200

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')

from exercise import routes

@app.route('/exercise/')
def exercise():
  return render_template('exercise.html')



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
