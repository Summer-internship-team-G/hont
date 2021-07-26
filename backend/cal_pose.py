import mediapipe as mp
import cv2
from celery import Celery
import os

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


pose_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]



# @celery.task()
def pose_pushup(): 
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
    l_ankle = results.pose_landmarks.landmark[27]
    r_ankle = results.pose_landmarks.landmark[28]

    return l_sh, r_sh, l_elbow, r_elbow, l_wrist,r_wrist, l_hip, r_hip, l_ankle, r_ankle

# @celery.task()
def pose_squat():
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
    l_hip = results.pose_landmarks.landmark[23]
    r_hip = results.pose_landmarks.landmark[24]
    l_knee = results.pose_landmarks.landmark[25]
    r_knee = results.pose_landmarks.landmark[26]
    l_foot = results.pose_landmarks.landmark[31]
    r_foot = results.pose_landmarks.landmark[32]

    return l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot
