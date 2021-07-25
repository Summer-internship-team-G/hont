from flask import Flask, Response, make_response, request, jsonify, abort, redirect
import json
from bson import json_util
from datetime import datetime
import math
import os
import numpy as np
import cv2
from flask_cors import cross_origin, CORS
import base64
#from PIL import Image
from pymongo import MongoClient
import mediapipe as mp
from functools import wraps
from werkzeug.utils import secure_filename
import uuid
from flask_restplus import Resource, Api
from celery import Celery
from flask_bcrypt import Bcrypt




# DOMAIN ="172.20.0.2"
# PORT = 27017
angle=-1
app = Flask(__name__)
api = Api(app, version='1.0', title='API title',
          description='A simple API',
          )
ns = api.namespace('custom', description='operations')


app.config.SWAGGER_UI_DOC_EXPANSION = 'full'


app.secret_key = b"'`D\x96\xf3m\xeb\x01b\x11\xb5\x05\x14S\x96\xbd"
CORS(app)
bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['MONGODB_SETTINGS'] = {
#     'host': os.environ['MONGODB_HOST'],
#     'username': os.environ['MONGODB_USERNAME'],
#     'password': os.environ['MONGODB_PASSWORD'],
#     'db': 'webapp'
# }
# client = MongoClient(
#         host = [ str(DOMAIN) + ":" + str(PORT) ],
#         serverSelectionTimeoutMS = 3000, # 3 second timeout
#         username = "admin",
#         password = "password",
#     )
client = MongoClient('mongodb://admin:password@mongodb')
db = client.webapp


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# db.init_app(app)
squat_guide = ""
pushup_guide= ""
squat_count = 0
pushup_count = 0
#==================================
#Pose Landmark Model 0부터 32번까지 
pose_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
action_status = True #스쿼트 중일 때 자세 
status = -1 #스쿼트 or 종료 
is_running = False
# squat_guide = [0 for i in range(3)] 
# pushup_guide = [0 for i in range(2)]



#각도 재는 함수
def get_angle_v3(p1, p2, p3):
    angle = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))
    return angle + 360 if angle < 0 else angle

#스쿼트 횟수 반환
def print_count():
    print("총 스쿼트",squat_count,"회")
    return squat_count

#스쿼트 가이드 반환
def print_guide():
    print(squat_guide)
    return squat_guide

##스쿼트 한 기준
def is_squat(hip_angle,l_knee_hip,r_knee_hip,l_knee_foot,r_knee_foot):
    global action_status
    global squat_count
    global squat_guide

    if 60 < hip_angle < 140 and l_knee_hip<=0.1 and r_knee_hip<=0.1 and l_knee_foot<=0.1 and r_knee_foot<=0.1:
      #  print("스쿼트 성공!")
        action_status = False

    else: #쉬고 있을때?
      #  print("스쿼트 실패ㅠㅠ")
        if action_status == False :
            squat_count+= 1
      #      print("스쿼트 개수 증가!!")
            action_status = True
            
        if hip_angle<60 :
            squat_guide +='엉덩이 높이를 올려주세요'
        if hip_angle>140:           
            squat_guide += '엉덩이 높이를 낮춰주세요'
        if l_knee_hip>0.1 or r_knee_hip>0.1:
            squat_guide += '허벅지가 바닥과 수평이 되도록 해주세요'
        if l_knee_foot > 0.1 or r_knee_foot > 0.1:
            squat_guide += '무릎이 발끝선을 넘지 않게 해주세요'

#스쿼트 - 올바른 스쿼트 자세 기준을 만든걸 던져줌
@celery.task()
def do_squat(shoulder_l, shoulder_r, hip_l, hip_r, knee_l, knee_r, foot_l, foot_r):
    global angle

    l_hip_angle = get_angle_v3(knee_l, hip_l, shoulder_l)
    r_hip_angle = get_angle_v3(knee_r, hip_r, shoulder_r)
    hip_angle = (l_hip_angle + r_hip_angle) / 2
    
    angle=hip_angle

    #knee-hip 계산 함수
    def squat_1(p1,p2):
        return round(abs(p1.y-p2.y),3) 
    l_knee_hip = squat_1(knee_l,hip_l)
    r_knee_hip = squat_1(knee_r,hip_r)

    #foot-knee 계산 함수
    def squat_2(p1,p2):
        return round(abs(p2.x-p1.x),3) 
    l_knee_foot = squat_2(knee_l,foot_l)
    r_knee_foot = squat_2(knee_r,foot_r)

  #  print("==========!!!!스쿼트 시작합니다!!!!==========")
    #프린토문 나중에 삭제하기 (테스트용)
  #  print("엉덩이 각도 ", round(hip_angle,2))
  #  print("무릎- 엉덩이 수평 ",l_knee_hip, r_knee_hip)
  #  print("무릎-발끝 ",l_knee_foot,r_knee_foot)
    
    is_squat(hip_angle,l_knee_hip,r_knee_hip,l_knee_foot,r_knee_foot)

##푸시업 한 기준

def is_pushup(elbow_angle, body_angle):
    global action_status
    global pushup_count
    global pushup_guide

    if 70 <= elbow_angle <= 100 and 160<= body_angle <= 200:
       # print("푸시업 성공!")
        action_status = False

    else: #쉬고 있을때?
      #  print("푸시업 실패ㅠㅠ")
        if action_status == False :
            pushup_count+= 1
       #     print("푸시업 개수 증가!!")
            action_status = True
            
        if elbow_angle < 70 :
            pushup_guide +='너무 내려가셨어요! 팔꿈치 각도를 90도로 맞춰주세요'
        if elbow_angle > 100:           
            pushup_guide += '조금 더 내려가주세요! 팔꿈치 각도를 90도로 맞춰주세요'
        if body_angle < 160:
            pushup_guide += '엉덩이를 내려서 몸이 일직선이 되도록 맞춰주세요'
        if body_angle > 200:
            pushup_guide += '엉덩이를 올려서 몸이 일직선이 되도록 맞춰주세요'

#푸시업 - 올바른 푸시업 자세 기준을 만든걸 던져줌
@celery.task()
def do_pushup(l_sh, r_sh, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_ankle, r_ankle):

    l_elbow_angle = get_angle_v3(l_wrist, l_elbow, l_sh)
    r_elbow_angle = get_angle_v3(r_wrist, r_elbow, r_sh)
    l_body_angle = get_angle_v3(l_sh, l_hip, l_ankle)
    r_body_angle = get_angle_v3(r_sh, r_hip, r_ankle)
    elbow_angle = (l_elbow_angle + r_elbow_angle) / 2
    body_angle = (l_body_angle + r_body_angle) / 2
    is_pushup(elbow_angle, body_angle)



# ############################################################################
#푸시업 분석 API
@app.route('/api/analyzePushup', methods=['POST'])
def analyze_pushup():
   
    image_file = request.files['file']
    image_file.save("posture.png")

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, static_image_mode=True)
    
    image = cv2.imread("posture.png")
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
   
   
    for index in pose_list:
        if results.pose_landmarks.landmark[index].visibility < 0.0001:
            results.pose_landmarks.landmark[index].x = 0
            results.pose_landmarks.landmark[index].y = 0
            results.pose_landmarks.landmark[index].z = 0

   
    l_sh = results.pose_landmarks.landmark[11]
    r_sh = results.pose_landmarks.landmark[12]
    l_elbow = results.pose_landmarks.landmark[13]
    r_elbow= results.pose_landmarks.landmark[14]
    l_wrist = results.pose_landmarks.landmark[15]
    r_wrist = results.pose_landmarks.landmark[16]
    l_hip = results.pose_landmarks.landmark[23]
    r_hip = results.pose_landmarks.landmark[24]
    l_knee = results.pose_landmarks.landmark[25]
    r_knee = results.pose_landmarks.landmark[26]
    l_ankle = results.pose_landmarks.landmark[27]
    r_ankle = results.pose_landmarks.landmark[28]
    l_foot = results.pose_landmarks.landmark[31]
    r_foot = results.pose_landmarks.landmark[32]
    
    global pushup_count
    global pushup_guide
    
    pushup_guide = ""
    
    do_pushup(l_sh, r_sh, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_ankle, r_ankle)
    

    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
    annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imwrite('./uploads/annotated_image.png', annotated_image)
    return jsonify({'count': pushup_count, "guide": pushup_guide})


# ############################################################################
#스쿼트 분석 API

@app.route('/api/analyzeSquat', methods=['POST'])
def analyze_squat():
   
    image_file = request.files['file']
    image_file.save("posture.png")

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, static_image_mode=True)
    
    image = cv2.imread("posture.png")
  
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
  
   
    for index in pose_list:
        if results.pose_landmarks.landmark[index].visibility < 0.0001:
            results.pose_landmarks.landmark[index].x = 0
            results.pose_landmarks.landmark[index].y = 0
            results.pose_landmarks.landmark[index].z = 0

   
    l_sh = results.pose_landmarks.landmark[11]
    r_sh = results.pose_landmarks.landmark[12]
    l_elbow = results.pose_landmarks.landmark[13]
    r_elbow= results.pose_landmarks.landmark[14]
    l_wrist = results.pose_landmarks.landmark[15]
    r_wrist = results.pose_landmarks.landmark[16]
    l_hip = results.pose_landmarks.landmark[23]
    r_hip = results.pose_landmarks.landmark[24]
    l_knee = results.pose_landmarks.landmark[25]
    r_knee = results.pose_landmarks.landmark[26]
    l_ankle = results.pose_landmarks.landmark[27]
    r_ankle = results.pose_landmarks.landmark[28]
    l_foot = results.pose_landmarks.landmark[31]
    r_foot = results.pose_landmarks.landmark[32]
    
    global squat_guide 
    global squat_count
    
    squat_guide = "" 
   
    do_squat(l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot)

    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
    annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imwrite('./uploads/annotated_image.png', annotated_image)
    return jsonify({'count': squat_count, "guide": squat_guide})       


######################## 사용자 api ########################

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    # try:
    #     payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
    #     is_blacklisted_token = check_blacklist(auth_token)
    #     if is_blacklisted_token:
    #         return 'Token blacklisted. Please log in again.'
    #     else:
    #         return payload['sub']
    # except jwt.ExpiredSignatureError:
    #     return 'Signature expired. Please log in again.'
    # except jwt.InvalidTokenError:
    #     return 'Invalid token. Please log in again.'

    payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
    is_blacklisted_token = check_blacklist(auth_token)
    if is_blacklisted_token:
        return 'Token blacklisted. Please log in again.'
    else:
        return payload['sub']


def check_blacklist(auth_token):
    # check whether auth token has been blacklisted
    res = db.blacklistTokens.find_one({"token" : str(auth_token)})
    if res:
        return True  
    else:
        return False

def remove_blacklist(auth_token):
    db.blacklistTokens.delete_many({"token": str(auth_token)})



class User:

    user_idx = 1

    def register(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        r_id = post_data.get('id', '')
        r_name = post_data.get('name', '')
        r_password = post_data.get('password', '')
        user = db.users.find_one({"id": r_id})
        
        if not user:
            try:
                r_pw = bcrypt.generate_password_hash(r_password).decode('utf-8')
                user = {
                    "user_idx": User.user_idx, # token에 넣을 user_idx
                    "name": r_name,
                    "id": r_id,
                    "password": r_pw
                }
                User.user_idx += 1
                # insert the user
                db.users.insert_one(user)
                # generate the auth token
                auth_token = encode_auth_token(user['user_idx'])
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.'
            }
            return make_response(jsonify(responseObject)), 202

    def login(self):
        # get the post data
        post_data = request.get_json()
        try:
            r_id = post_data.get('id', '')
            r_password = post_data.get('password', '')
            # fetch the user data
            user = db.users.find_one({"id": r_id})
            if user and bcrypt.check_password_hash(user['password'], r_password):
                auth_token = encode_auth_token(user['user_idx'])
                if auth_token:
                    remove_blacklist(auth_token) # 블랙리스트에서 삭제
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500

    def checkAuth(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = db.users.find_one({"user_idx": resp})
                if user:
                    responseObject = {
                        'status': 'success',
                        'data': {
                            'name': user['name'],
                            'id': user['id']
                        }
                    }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

    def logout(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token) 
            if not isinstance(resp, str):
            # if db.users.find_one({"user_idx": resp}):
                # mark the token as blacklisted
                try:
                    # insert the token
                    db.blacklistTokens.insert_one({"token": str(auth_token)})
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403


@app.route('/auth/register', methods=['POST'])
def register():
    return User().register()

@app.route('/auth/register', methods=['POST'])
def login():
    return User().login()

@app.route('/auth/status')
def checkAuth():
    return User().checkAuth()

@app.route('/auth/logout', methods=['POST'])
def logout():
    return User().logout()

####################### 운동 api ########################

class Exercise:

    def updateExercise(self):
        # print(request.is_json)
        exercise = request.get_json()
        # exercise = {
        #     "id": 
        #     "exerDate": "2020-07-14"
        #     "exerType": "1" or "2"
        #     "exerNum": 정수
        #     "exerTime": 정수 (초 단위)  
        # }

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
            # print("-------------")
            # print("값 존재!:", cursor.count())
            # print("-------------")
            # result_dict = {}
            # key = 0
            # for doc in cursor:
            #     key += 1
            #     result_dict[str(key)] = {
            #         "squatNum": doc["squatNum"],
            #         "pushupNum": doc["pushupNum"],
            #         "exerTime": doc["exerTime"]
            #         }
            #     print(result_dict[str(key)])
            # print("-------------")
            # print(result_dict)
            # print(type(result_dict))
            
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
            # print(result_dict)
            return jsonify(result_dict), 200
        else:
            # print("값 없음:", cursor.count())
            return jsonify( {"error": "No workout records" }), 402
# db.exercises.document = {
#     "id": "~~",
#     "exerDate": "2021-07-14",
#     "squatNum": 정수,
#     "pushupNum": 정수,
#     "everTime": 정수 (초 단위)
# }

@app.route('/recordex', methods=['POST'])
def updateExercise():
    return Exercise().updateExercise()

@app.route('/exercise/statistics', methods=['POST'])
def showExercises():
    return Exercise().showExercises()



####################### rest api ########################
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
        
if __name__ == '__main__':
    # only used locally
    app.run(host='0.0.0.0', port=5000, debug=True)
