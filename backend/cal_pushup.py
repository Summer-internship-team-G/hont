import math

#각도 재는 함수
def get_angle_v3(p1, p2, p3):
	angle = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))
	return angle + 360 if angle < 0 else angle

##푸시업 한 기준

def is_pushup(elbow_angle, body_angle):
	print("======is_pushup start=======")
	pushup_guide= ""
	action_status = True

	if 60 <= elbow_angle <= 120:
		action_status = False

	else: 
		if action_status == False:
			action_status = True


		if elbow_angle < 60:
			pushup_guide +='너무 내려가셨어요! 팔꿈치 각도를 90도로 맞춰주세요\n'
		if elbow_angle > 120:           
			pushup_guide += '조금 더 내려가주세요! 팔꿈치 각도를 90도로 맞춰주세요\n'
		# if body_angle < 160:
		# 	pushup_guide += '엉덩이를 내려서 몸이 일직선이 되도록 맞춰주세요\n'
		# if body_angle > 200:
		# 	pushup_guide += '엉덩이를 올려서 몸이 일직선이 되도록 맞춰주세요\n'

	if not action_status:
		text = "성공"
	else:
		text = "실패"
	print("======is_pushup end=====")
	
	return action_status, pushup_guide, text

#푸시업 - 올바른 푸시업 자세 기준을 만든걸 던져줌
def do_pushup(l_sh, r_sh, l_elbow, r_elbow, l_wrist, r_wrist, l_hip, r_hip, l_ankle, r_ankle):

	l_elbow_angle = get_angle_v3(l_wrist, l_elbow, l_sh)
	r_elbow_angle = get_angle_v3(r_wrist, r_elbow, r_sh)
	l_body_angle = get_angle_v3(l_sh, l_hip, l_ankle)
	r_body_angle = get_angle_v3(r_sh, r_hip, r_ankle)
	elbow_angle = (l_elbow_angle + r_elbow_angle) / 2
	body_angle = (l_body_angle + r_body_angle) / 2

	p_count, p_guide, text = is_pushup(elbow_angle, body_angle)

	return p_count, p_guide, text

