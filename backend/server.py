from flask import Flask, request, jsonify
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


######################## 푸시업 분석 API ########################
@app.route('/api/analyzePushup', methods=['POST'])
def analyze_pushup():
   
    image_file = request.files['file']
    image_file.save("posture.png")

   
    l_sh, r_sh, l_elbow, r_elbow, l_wrist,r_wrist, l_hip, r_hip, l_ankle, r_ankle = pose_pushup()
    count, guide = do_pushup(l_sh, r_sh, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_ankle, r_ankle)

    return jsonify({'count': count, "guide": guide})


######################## 스쿼트 분석 API ########################
@app.route('/api/analyzeSquat', methods=['POST'])
def analyze_squat():
   
    image_file = request.files['file']
    image_file.save("posture.png")

    l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot = pose_squat()
    count, guide = do_squat(l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot)

    return jsonify({'count': count, "guide": guide})       

######################## 운동 관련 API ########################

@app.route('/recordex', methods=['POST'])
def updateExercise():
    return Exercise().updateExercise()

@app.route('/exercise/statistics', methods=['POST'])
def showExercises():
    return Exercise().showExercises()


######################## 사용자 API ########################
@app.route('/auth/register', methods=['POST'])
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
