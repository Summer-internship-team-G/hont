from flask import Flask, jsonify, request
from app import db

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

        preNum, preTime = 0, 0
        if exercise['exerType'] == "1":
            if db.exercises.find_one({"id": exercise['id'], "exerDate": exercise['exerDate']}):
                pre = db.exercises.find_one({"id": exercise['id'], "exerDate": exercise['exerDate']})
                preNum = pre['squartNum']
                preTime = pre['exerTime']
            db.exercises.update_one(
                {"id": exercise['id'], "exerDate": exercise['exerDate'] },
                {"$set": {"squartNum": preNum + exercise['exerNum'], "exerTime": preTime + exercise['exerTime']}}, 
                upsert = True
            )
        else:
            if db.exercises.find_one({"id": exercise['id'], "exerDate": exercise['exerDate']}):
                pre = db.exercises.find_one({"id": exercise['id'], "exerDate": exercise['exerDate']})
                preNum = pre['pushupNum']
                preTime = pre['exerTime']
            db.exercises.update_one(
                {"id": exercise['id'], "exerDate": exercise['exerDate'] },
                {"$set": {"pushupNum": preNum + exercise['exerNum'], "exerTime": preTime + exercise['exerTime']}}, 
                upsert = True
            )

        return jsonify(exercise), 200

    def showExercises(self):
        user_info = request.get_json()
        
        exercises = db.exercise.find_one({"id": user_info['id'], "exerDate": user_info['exerDate']})
        if exercises:
            return jsonify(exercises), 200
        return jsonify({ "error": "No workout records" }), 402

# db.exercises.document = {
#     "id": "~~",
#     "exerDate": "2021-07-14",
#     "squarNum": 정수,
#     "pushupNum": 정수,
#     "everTime": 정수 (초 단위)
# }