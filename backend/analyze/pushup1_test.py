#메인 함수 : exercising
#스쿼트 횟수 변수: squat_count / 횟수 프린트 함수: print_count()
#가이드 함수 3개 : hip_angle_guide()/ knee_hip_guide() / knee_foot_guide()

import mediapipe as mp
import cv2
import math
import sys
#==================================
#Pose Landmark Model 0부터 32번까지 
pose_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
action_status = True #스쿼트 중일 때 자세 
squat_count = 0  #스쿼트 개수 
status = -1 #스쿼트 or 종료 
is_running = False
squat_guide = [0 for i in range(3)]
#==================================

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

    if 80 < hip_angle < 100 and l_knee_hip<=0.1 and r_knee_hip<=0.1 and l_knee_foot<=0.1 and r_knee_foot<=0.1:
        print("스쿼트 성공!")
        action_status = False

    else: #쉬고 있을때?
        print("스쿼트 실패ㅠㅠ")
        if action_status == False :
            squat_count+= 1
            print("스쿼트 개수 증가!!")
            action_status = True
            
        if hip_angle<80 :
            squat_guide[0] ='엉덩이 높이를 올려주세요'            
        if hip_angle>100:           
            squat_guide[0] = '엉덩이 높이를 낮춰주세요'
        if l_knee_hip>0.1 or r_knee_hip>0.1:
            squat_guide[1] = '허벅지가 바닥과 수평이 되도록 해주세요'
        if l_knee_foot > 0.1 or r_knee_foot > 0.1:
            squat_guide[2] = '무릎이 발끝선을 넘지 않게 해주세요'

#스쿼트 - 올바른 스쿼트 자세 기준을 만든걸 던져줌
def do_squat(shoulder_l, shoulder_r, hip_l, hip_r, knee_l, knee_r, foot_l, foot_r):

    l_hip_angle = get_angle_v3(knee_l, hip_l, shoulder_l)
    r_hip_angle = get_angle_v3(knee_r, hip_r, shoulder_r)
    hip_angle = (l_hip_angle + r_hip_angle) / 2
    
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

    print("==========!!!!스쿼트 시작합니다!!!!==========")
    #프린토문 나중에 삭제하기 (테스트용)
    print("엉덩이 각도 ", round(hip_angle,2))
    print("무릎- 엉덩이 수평 ",l_knee_hip, r_knee_hip)
    print("무릎-발끝 ",l_knee_foot,r_knee_foot)
    
    is_squat(hip_angle,l_knee_hip,r_knee_hip,l_knee_foot,r_knee_foot)

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
        l_hip = results.pose_landmarks.landmark[23]
        r_hip = results.pose_landmarks.landmark[24]
        l_knee = results.pose_landmarks.landmark[25]
        r_knee = results.pose_landmarks.landmark[26]
        l_foot = results.pose_landmarks.landmark[31]
        r_foot = results.pose_landmarks.landmark[32]
        #=================================================
            #if not results.pose_landmarks:
            #    continue
        
        do_squat(l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot)
        print_count()
        print_guide()
        squat_guide=[0 for i in range(3)]

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


    #################

'''
#exercising 함수 시작 
def exercising(): 
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    #감지가 성공한 것으로 간주되는 사람 감지 모델의 최소 신뢰도 값 = 0.5 기본값
    #포즈 랜드 마크가 성공적으로 추적 된 것으로 간주되도록 랜드 마크 추적 모델의 최소 신뢰도 값 = 0.5 기본값
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # 웹캠으로 사용
    #cap = cv2.VideoCapture(0)

    #사용자가 시작 버튼 눌렀을 때부터 종료 버튼 누를 때까지.
    #while cap.isOpened():
    global is_running #초기값 false -> 스쿼트 선택 -> true 
    global action_status 
    global squat_guide

    if is_running == False:
        status = int(input("스쿼트 1, 푸시업 2, 종료 3:"))
        is_running = True
        action_status = True 
    else:
        pass

    success, image = cv2.imread("squat1.png") #cap.read()
    if not success:
        print("카메라가 인식되지않습니다.")
        #continue            
    # 이미지를 좌우 반전을 시키고 BGR형태의 이미지를 RGB로 변환하여 활용합니다.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # 해당 영역에서 입력된 이미지를 분석하여 결과값을 도출해줍니다.    
    results = pose.process(image)
    try:
        for index in pose_list:
            if results.pose_landmarks.landmark[index].visibility < 0.0001:
                results.pose_landmarks.landmark[index].x = None
                results.pose_landmarks.landmark[index].y = None
                results.pose_landmarks.landmark[index].z = None

        #==================================================
        l_sh = results.pose_landmarks.landmark[11]
        r_sh = results.pose_landmarks.landmark[12]
        l_hip = results.pose_landmarks.landmark[23]
        r_hip = results.pose_landmarks.landmark[24]
        l_knee = results.pose_landmarks.landmark[25]
        r_knee = results.pose_landmarks.landmark[26]
        l_foot = results.pose_landmarks.landmark[31]
        r_foot = results.pose_landmarks.landmark[32]
        #=================================================
        if status == 1:
            # ================스쿼트=================
            ## 각 운동마다 필요한 부위만 받아감(11 12 23 24 25 26 31 32) **
            do_squat(l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot)
            print_count()
            print_guide()
            squat_guide=[0 for i in range(3)]
        #elif status == 2 :
            #================푸시업==================

        elif status == 3:
            return -1
                    
        else:
            print("다른 값을 넣으세요.")
                
    except Exception as e:
        pass
    #    print(e)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 이미지에 result에 저장된 좌표에 맞게 landmark를 표시합니다.
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)   
        
            
    if cv2.waitKey(5) & 0xFF == 27:
        is_running = False
        #break

    pose.close()
    #cap.release()

if __name__ == "__main__":
    exercising()



'''
