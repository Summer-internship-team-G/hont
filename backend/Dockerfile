FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /server
COPY server.py ./
COPY cal_pose.py ./
COPY cal_squat.py ./
COPY cal_pushup.py ./
COPY record_exercise.py ./
COPY search.py ./
COPY tts.py ./
COPY user.py ./
EXPOSE 5000

CMD python server.py

