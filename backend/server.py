from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
import mediapipe as mp
from flask_restplus import Api, Resource
from flask_bcrypt import Bcrypt
from cal_squat import do_squat
from cal_pushup import do_pushup
from cal_pose import pose_squat, pose_pushup
from record_exercise import Exercise
from user import User
import boto3
import os
from celery import Celery

app = Flask(__name__)
api = Api(app, version='1.0', title='API title',
          description='A simple API',
          )
ns = api.namespace('custom', description='operations')


app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.debug = True
app.secret_key = b"'`D\x96\xf3m\xeb\x01b\x11\xb5\x05\x14S\x96\xbd"


CORS(app)
bcrypt = Bcrypt(app)
client = MongoClient('mongodb://admin:password@mongodb')
db = client.webapp

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'mongodb://localhost:27017/webapp')
celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


######################## 푸시업 분석 API ########################

class Pushup:
    pushup_count = 0
    def analyze_pushup(self):
        image_file = request.files['file']
        image_file.save("posture.png")
        l_sh, r_sh, l_elbow, r_elbow, l_wrist,r_wrist, l_hip, r_hip, l_ankle, r_ankle = pose_pushup()
        status, guide, text = do_pushup(l_sh, r_sh, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_ankle, r_ankle)
        if not status:
            Pushup.pushup_count += 1
        return jsonify({'count': Pushup.pushup_count, "guide": guide, "text": text})

@app.route('/api/analyzePushup', methods=['POST'])
def analyze_pushup():
   return Pushup().analyze_pushup()


######################## 스쿼트 분석 API ########################

class Squat:
    squat_count = 0
    def analyze_squat(self):
        image_file = request.files['file']
        image_file.save("posture.png")
        l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot = pose_squat()
        status, guide, text = do_squat(l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot)
        if not status:
            Squat.squat_count += 1
        return jsonify({'count': Squat.squat_count, "guide": guide, "text": text})

@app.route('/api/analyzeSquat', methods=['POST'])
def analyze_squate():
    return Squat().analyze_squat()

######################## 운동 관련 API ########################

@app.route('/recordex', methods=['POST'])
@celery.task()
def updateExercise():
    return Exercise().updateExercise()

@app.route('/exercise/statistics', methods=['POST'])
def showExercises():
    return Exercise().showExercises()


######################## 사용자 API ########################
@app.route('/auth/register', methods=['POST'])
@celery.task()
def register():
    return User().register()

@app.route('/auth/login', methods=['POST'])
def login():
    return User().login()

@app.route('/auth/status')
def checkAuth():
    return User().checkAuth()

@app.route('/auth/logout', methods=['POST'])
def logout():
    return User().logout()

####################### TTS api ########################
def connectToPolly():
    region_name = 'ap-northeast-2'
    polly_client = boto3.client(
        'polly',
        aws_access_key_id = 'AKIAU6ECZPVOP6A4VROO',
        aws_secret_access_key = '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',
        region_name = region_name
    )
    return polly_client

@app.route('/textToSpeech/<int:count>', methods=['GET'])
def textToSpeech(count):
    print("=== textToSpeech start ====")

    polly_client = connectToPolly()
    response = polly_client.synthesize_speech(
        Text="<speak>" + str(count) + "</speak>",    
        VoiceId='Seoyeon',
        OutputFormat='mp3',
        TextType='ssml'
        )

    return send_file(response.get("AudioStream"), mimetype="audio/mp3")

######################## swagger ########################
@ns.route('/<string:text>')
@ns.response(200, 'Found')
@ns.response(404, 'Not found')
@ns.response(500, 'Internal Error')
class Functions(Resource):
    @api.doc('get')
    def get(self, text):
        return '', 404

    @api.doc('delete')
    def delete(self, id):
        return '', 404

    @api.doc('put')
    def put(self, id):
        return '', 404
    @api.doc('post')
    def post(self, id):
        return '', 404
        
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
