import math

#각도 재는 함수
def get_angle_v3(p1, p2, p3):
    angle = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))
    return angle + 360 if angle < 0 else angle

##스쿼트 한 기준
def is_squat(hip_angle,l_knee_hip,r_knee_hip,l_knee_foot,r_knee_foot):
    print("======is_squat start=======")
    squat_guide = ""
    action_status = True 
    
    if 60 < hip_angle < 180 and l_knee_hip<=0.2 and r_knee_hip<=0.2 and l_knee_foot<=0.1 and r_knee_foot<=0.1:
        print("스쿼트 성공!")
        action_status = False
        print("hip_agle:"+str(hip_angle)+"l_knee_hip:"+str(l_knee_hip))
        print("r_knee_hip:"+str(r_knee_hip)+"l_knee_foot:"+str(l_knee_foot))
        print("r_knee_foot"+str(r_knee_foot))

    else: #쉬고 있을때?
        # print("스쿼트 실패ㅠㅠ")
        if action_status == False :
            # print("스쿼트 개수 증가!!")
            action_status = True
            
        if hip_angle<60 :
            squat_guide +='엉덩이 높이를 올려주세요\n'
            # print("엉덩이 각도"+str(hip_angle))
        if hip_angle>180:           
            squat_guide += '엉덩이 높이를 낮춰주세요\n'
            # print("엉덩이 각도"+str(hip_angle))
        if l_knee_hip>0.2 or r_knee_hip>0.2:
            squat_guide += '허벅지가 바닥과 수평이 되도록 해주세요\n'
            # print("허벅지가 바닥과 수평이 되도록 해주세요")
        if l_knee_foot > 0.1 or r_knee_foot > 0.1:
            squat_guide += '무릎이 발끝선을 넘지 않게 해주세요\n'
            # print("무릎이 발끝선을 넘지 않게 해주세요")

    if not action_status:
        text = "성공"
    else:
        text = "실패"
    print("======is_squat end=======")
    
    return action_status, squat_guide, text

#스쿼트 - 올바른 스쿼트 자세 기준을 만든걸 던져줌
# @celery.task()
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
    
    count, guide, text = is_squat(hip_angle,l_knee_hip,r_knee_hip,l_knee_foot,r_knee_foot)
    return count, guide, text