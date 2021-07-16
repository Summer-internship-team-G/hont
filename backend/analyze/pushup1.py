#메인 함수 : exercising
#스쿼트 횟수 변수: squat_count / 횟수 프린트 함수: print_count()
#가이드 함수 3개 : hip_angle_guide()/ knee_hip_guide() / knee_foot_guide()

import mediapipe as mp
import cv2
import math

#==================================
#Pose Landmark Model 0부터 32번까지 
pose_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
action_status = True #푸시업 중일 때 자세 
pushup_count = 0  #푸시업 개수 
status = -1 #푸시업 or 종료 
is_running = False
pushup_guide = [0 for i in range(2)]
#==================================

#각도 재는 함수
def get_angle_v3(p1, p2, p3):
    angle = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))
    return angle + 360 if angle < 0 else angle

#푸시업 횟수 반환
def print_count():
    print("총 푸시업",pushup_count,"회")
    return pushup_count

#푸시업 가이드 반환
def print_guide():
    print(pushup_guide)
    return pushup_guide

##푸시업 한 기준
def is_pushup(elbow_angle, body_angle):
    global action_status
    global pushup_count
    global pushup_guide

    if 70 <= elbow_angle <= 100 and 160<= body_angle <= 200:
        print("푸시업 성공!")
        action_status = False

    else: #쉬고 있을때?
        print("푸시업 실패ㅠㅠ")
        if action_status == False :
            pushup_count+= 1
            print("푸시업 개수 증가!!")
            action_status = True
            
        if elbow_angle < 70 :
            pushup_guide[0] ='너무 내려가셨어요! 팔꿈치 각도를 90도로 맞춰주세요'
        if elbow_angle > 100:           
            pushup_guide[0] = '조금 더 내려가주세요! 팔꿈치 각도를 90도로 맞춰주세요'
        if body_angle < 160:
            pushup_guide[1] = '엉덩이를 내려서 몸이 일직선이 되도록 맞춰주세요'
        if body_angle > 200:
            pushup_guide[1] = '엉덩이를 올려서 몸이 일직선이 되도록 맞춰주세요'

#푸시업 - 올바른 푸시업 자세 기준을 만든걸 던져줌
def do_pushup(l_sh, r_sh, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_ankle, r_ankle):

    l_elbow_angle = get_angle_v3(l_wrist, l_elbow, l_sh)
    r_elbow_angle = get_angle_v3(r_wrist, r_elbow, r_sh)
    l_body_angle = get_angle_v3(l_sh, l_hip, l_ankle)
    r_body_angle = get_angle_v3(r_sh, r_hip, r_ankle)
    elbow_angle = (l_elbow_angle + r_elbow_angle) / 2
    body_angle = (l_body_angle + r_body_angle) / 2
    
    #프린토문 나중에 삭제하기 (테스트용)
    print("==========!!!!푸시업 시작합니다!!!!==========")
    print("팔꿈치 각도 {0}".format(round(elbow_angle,2)))
    print("몸 각도 {0}".format(round(body_angle,2)))
    
    is_pushup(elbow_angle, body_angle)

#exercising 함수 시작 
def exercising(): 
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    #감지가 성공한 것으로 간주되는 사람 감지 모델의 최소 신뢰도 값 = 0.5 기본값
    #포즈 랜드 마크가 성공적으로 추적 된 것으로 간주되도록 랜드 마크 추적 모델의 최소 신뢰도 값 = 0.5 기본값
    pose = mp_pose.Pose(min_detection_confidence=0.5, static_image_mode=True)

    # For static images:    
    IMAGE_FILES = ["squat_img1.jpeg"]
        
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        #image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        #try:
        for index in pose_list:
            if results.pose_landmarks.landmark[index].visibility < 0.0001:
                results.pose_landmarks.landmark[index].x = None
                results.pose_landmarks.landmark[index].y = None
                results.pose_landmarks.landmark[index].z = None


        #==================================================
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

        #=================================================
            #if not results.pose_landmarks:
            #    continue
        
        do_pushup(l_sh, r_sh, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_ankle, r_ankle)
        print_count()
        print_guide()
        pushu_guide=[0 for i in range(2)]

        #except Exception as e:
         #   pass

            
        
        # Draw pose landmarks on the image.
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(
        annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
        # Plot pose world landmarks.
        #mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

if __name__ == "__main__":
    exercising()


####################

