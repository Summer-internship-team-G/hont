import mediapipe as mp
import cv2
import math
import time
import threading

#==================================
#Pose Landmark Model 0부터 32번까지 
pose_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
action_status = True #쉬는중
action_count = 0
status = -1
is_running = False
#==================================
result_list = []
#==================================


#각도 재는 함수
def get_angle_v3(p1, p2, p3): #라디안으로 표기
    angle = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))
    return angle + 360 if angle < 0 else angle

#스쿼트 
def do_squat(shoulder_l, shoulder_r, hip_l, hip_r, knee_l, knee_r, foot_l, foot_r):
    
    print("==========!!!!스쿼트 시작합니다!!!!==========")
    global action_status
    global action_count

    l_hip_angle = get_angle_v3(knee_l, hip_l, shoulder_l)
    r_hip_angle = get_angle_v3(knee_r, hip_r, shoulder_r)
    hip_angle = (l_hip_angle + r_hip_angle) / 2
    
    #1. 무릎-엉덩이랑 일직선 => l_knee의 y좌표, l_hip의 y좌표 일치 / r_knee의 y좌표, r_hip의 y좌표 일치
    #2. 무릎이 발끝선을 넘지 않게  => l_knee의 x좌표, l_foot의 x좌표 일치 / r_knee의 x좌표, r_foot의 x좌표 일치
    #3. 엉덩이 각도 => knee, hip,shoulder 
    #==> knee, hip,foot,shoulder

    
    #p1,p2에 무릎, 엉덩이 넣기, 왼쪽버전 오른쪽 버전 둘다 
    def squat_1(p1,p2):
        return round(abs(p1.y-p2.y),3) #knee-hip 
    l_knee_hip = squat_1(knee_l,hip_l)
    r_knee_hip = squat_1(knee_r,hip_r)

    def squat_2(p1,p2):
        return round(abs(p2.x-p1.x),3) #foot-knee (왼쪽 측면 기준)
    l_knee_foot = squat_2(knee_l,foot_l)
    r_knee_foot = squat_2(knee_r,foot_r)

    print(" 엉덩이 각도 ", round(hip_angle,2))
    print("무릎- 엉덩이 수평",l_knee_hip, r_knee_hip)
    print("무릎-발끝 ",l_knee_foot,r_knee_foot)


    ##스쿼트 한 기준
    if 80 < hip_angle < 140 and l_knee_hip<=0.1 and r_knee_hip<=0.1 and l_knee_foot<=0.1 and r_knee_foot<=0.1:
        print("스쿼트 성공!")
        action_status = False
    else: #쉬고 있을때?
        print("스쿼트 실패ㅠㅠ")
        print("총 스쿼트",action_count,"회")
        if action_status == False:
            action_count+= 1
            print("스쿼트 개수 증가!!")
            print("총 스쿼트",action_count,"회")
            action_status = True
        if hip_angle<80 or hip_angle>140:
            print("엉덩이 각도를 조절해주세요")
        if l_knee_hip>0.1 or r_knee_hip>0.1:
            print("허벅지가 바닥과 수평이 되도록 해주세요")
        if l_knee_foot > 0.1 or r_knee_foot > 0.1:
            print("무릎이 발끝선을 넘지 않게 해주세요")
    #time.sleep(3)
    #threading.Timer(0.5, is_squat(shoulder_l, shoulder_r, hip_l, hip_r, knee_l, knee_r, foot_l, foot_r)).start()


#exercising 함수 시작 
def exercising(): 
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    #감지가 성공한 것으로 간주되는 사람 감지 모델의 최소 신뢰도 값 = 0.5 기본값
    #포즈 랜드 마크가 성공적으로 추적 된 것으로 간주되도록 랜드 마크 추적 모델의 최소 신뢰도 값 = 0.5 기본값
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # 웹캠으로 사용
    cap = cv2.VideoCapture(0)

    #사용자가 시작 버튼 눌렀을 때부터 종료 버튼 누를 때까지.
    while cap.isOpened():
        global is_running #초기값 false -> 운동종류 선택 -> true 
        global action_status 

        if is_running == False:
            status = int(input("스쿼트 0, 종료 1:"))
            is_running = True
            action_status = True 
        else:
            pass

        success, image = cap.read()
        if not success:
            print("카메라가 인식되지않습니다.")
            continue            
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
            
            if status == 0:
                # ================스쿼트=================
                ## 각 운동마다 필요한 부위만 받아감 **
                #11 12 23 24 25 26 31 32
                do_squat(l_sh, r_sh, l_hip, r_hip, l_knee, r_knee, l_foot, r_foot)
                

              

            elif status == 1:
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
            break

    pose.close()
    cap.release()

if __name__ == "__main__":
    exercising()