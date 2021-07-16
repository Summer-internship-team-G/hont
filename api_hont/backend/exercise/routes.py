from flask import Flask
from app import app
from exercise.models import Exercise

@app.route('/api/update', methods=['POST'])
def updateExercise():
    return Exercise().updateExercise()


@app.route('/exercise/statistics')
def showExercises():
    return Exercise().showExercises()