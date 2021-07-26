from flask import Flask, request, jsonify, redirect, make_response
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.debug = True
app.secret_key = b"'`D\x96\xf3m\xeb\x01b\x11\xb5\x05\x14S\x96\xbd"
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['UPLOAD_FOLDER'] = 'uploads'
bcrypt = Bcrypt(app)
client = MongoClient('mongodb://admin:password@mongodb')
db = client.webapp
####################### 운동 ########################

class Exercise:

    def updateExercise(self):
        exercise = request.get_json()

        if exercise['exerType'] == "1":
            db.exercises.insert({"id": exercise['id'], "exerDate": exercise['exerDate'], "squatNum": exercise['exerNum'], "pushupNum": 0, "exerTime": exercise['exerTime']})
        else:
            db.exercises.insert({"id": exercise['id'], "exerDate": exercise['exerDate'], "squatNum": 0, "pushupNum":  exercise['exerNum'], "exerTime": exercise['exerTime']})
        return jsonify(exercise), 200

    def showExercises(self):
        user_info = request.get_json()
        r_id = user_info['id']
        r_exerDate= user_info['exerDate']
        cursor = db.exercises.find({"id": r_id, "exerDate": r_exerDate})

        if cursor.count():
            result_dict = {}
            key = "key"
            value = []
            for doc in cursor:
                value.append({
                    "squatNum": doc["squatNum"],
                    "pushupNum": doc["pushupNum"],
                    "exerTime": doc["exerTime"]
                })
            result_dict[key] = value
            print(result_dict)
            return jsonify(result_dict), 200
        else:
            return jsonify( {"error": "No workout records" }), 402