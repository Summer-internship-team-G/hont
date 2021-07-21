from flask import Flask, Response,render_template, request, jsonify, abort, session, redirect
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
from passlib.hash import pbkdf2_sha256
import uuid
from flask_restplus import Resource, Api
from celery import Celery




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

# Decorators

def login_required(function_to_protect):
  @wraps(function_to_protect)
  def wrapper(*args, **kwargs):
    user_id = session.get("_id")
    if user_id:
      if db.users.find_one({ "_id": user_id }): # db에 존재
        return function_to_protect(*args, **kwargs)
      else:
        return jsonify({ "error": "true" }), 400 # db에 회원 정보 없음 -> user/signup
    else:
      return jsonify({ "error": "true" }), 400 # 로그인 되지 않음 -> user/login
  return wrapper

@app.route('/checkLogin')
@login_required
def LoggedIn():
  return jsonify({ "error": "false" }), 200


class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['id'] = user['id']
    session['_id'] = user['_id']
    return jsonify(user), 200

  def signup(self):
    data = request.get_json()
    r_name = data.get('name','')
    r_id = data.get('id', '')
    r_pass = data.get('password', '')

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": r_name,
      "id": r_id,
      "password": r_pass
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "id": user['id'] }):
      return jsonify({ "error": "ID already in use" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": 1 }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):
    data = request.get_json()
    r_id = data.get('id','')
    r_pass = data.get('password', '')
    user = db.users.find_one({
      "id": r_id
    })
    print("------------")
    print(r_id)
    print(r_pass)
    if user and pbkdf2_sha256.verify(r_pass, user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "true" }), 401

  def withdrawal(self):
    data = request.get_json()
    r_pass = data.get('password', '')
    user = db.users.find_one({ "_id": session['_id'] })
    if user and pbkdf2_sha256.verify(r_pass, user['password']):
      db.users.delete_one({ "id": user['id'] })
      db.exercises.delete_many({ "id": user['id'] })
      return self.signout()
    return jsonify({ "error": "Incorrect password" }), 402

class Exercise:

    def updateExercise(self):
        print(request.is_json)
        exercise = request.get_json()

        # exercise = {
        #     "id": 
        #     "exerDate": "2020-07-14"
        #     "exerType": "1" or "2"
        #     "exerNum": 정수
        #     "exerTime": 정수 (초 단위)  
        # }
        
        # db.exercises에 id, exerDate가 일치하는 운동 기록 검색
        # 만약 일치하는 운동 기록 이미 있다면 squarNum/pushupNum, everTime을 preNum, preTime변수에 저장
        # db의 squarNum/pushNum, exerTime 갱신
        result = "false"
        prePN, preSN, preTime = 0, 0, 0
        if db.exercises.find_one({"id": exercise['id'], "exerDate": exercise['exerDate']}):
            pre = db.exercises.find_one({"id": exercise['id'], "exerDate": exercise['exerDate']})
            prePN = pre['pushupNum']
            preSN = pre['squartNum']
            preTime = pre['exerTime']
        if exercise['exerType'] == "1":
            db.exercises.update_one(
                {"id": exercise['id'], "exerDate": exercise['exerDate'] },
                {"$set": {"squartNum": preSN + exercise['exerNum'], "pushupNum": prePN, "exerTime": preTime + exercise['exerTime']}}, 
                upsert = True
            )
        else:
            db.exercises.update_one(
                {"id": exercise['id'], "exerDate": exercise['exerDate'] },
                {"$set": {"squartNum": preSN, "pushupNum": prePN + exercise['exerNum'], "exerTime": preTime + exercise['exerTime']}}, 
                upsert = True
            )

        return jsonify(exercise), 200


    def showExercises(self):
        user_info = request.get_json()
        
        exercises = db.exercise.find_one({"id": user_info['id'], "exerDate": user_info['exerDate']})
        if exercises:
            return jsonify(exercises), 200
        return jsonify({ "error": "No workout records" }), 402

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/exercise/')
def exercise():
  return render_template('exercise.html')

@app.route('/recordex', methods=['POST'])
def updateExercise():
    return Exercise().updateExercise()


@app.route('/exercise/statistics')
def showExercises():
    return Exercise().showExercises()

if __name__ == '__main__':
    # only used locally
    app.run(host='0.0.0.0', port=5000, debug=True)
