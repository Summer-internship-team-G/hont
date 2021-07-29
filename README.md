# ❗❗❗2021 Summer SilliconValley Internship Project❗❗❗ 
> **💪HONT : 혼자 + Training**
> > HONT is a project that counts the number of exercises and provides exercise times, statistics on the day, suitable exercise searches by body part, and guidelines for those who exercise alone.

## 📝Index
> <b><a href="#system-architecture">System Architecture</a></b>
>  
> <b><a href="#development-stack">Development Stack</a></b> 
> 
> <b><a href="#demo-video">Demo Video</a></b>  
> 
> <b><a href="#frontend">Frontend</a></b>  
> 
> <b><a href="#backend">Backend</a></b>
> 
> <b><a href="#AI">AI</a></b>  
> 
> <b><a href="#contributors">Contributors</a></b>   
> 
> <b><a href="#docker-prerequisites">Docker Prerequisites</a></b>  

## ⚙System Architecture
![System Architecture](https://user-images.githubusercontent.com/34560965/127418871-6adb856a-9ef8-4423-9559-0b3ac1999172.png)


## 🛠Development Stack
<p align="center">
  <img src="https://img.shields.io/badge/react-17.0.2-blue" />
  <img src="https://img.shields.io/badge/flask-1.1.1-blue" />
  <img src="https://img.shields.io/badge/gunicorn-20.0.4-blue" />
  <img src="https://img.shields.io/badge/OpenCV-4.5.3-blue" />
  <img src="https://img.shields.io/badge/MongoDB-blue" />
  <img src="https://img.shields.io/badge/redis-blue" />
  <img src="https://img.shields.io/badge/Celery-blue" />
  <img src="https://img.shields.io/badge/Docker-blue" />
  <img src="https://img.shields.io/badge/Swagger-blue" />
  <img src="https://img.shields.io/badge/VSCode-blue" />
</p>
<p align="center" text-align="center" width="100%">
  <img src="https://img.shields.io/github/contributors/Summer-internship-team-G/hont" />
  <img src="https://img.shields.io/github/last-commit/Summer-internship-team-G/hont?color=red" />
  <img src="https://img.shields.io/github/commit-activity/w/Summer-internship-team-G/hont?color=red" />
</p>

## 💎Presentation file
https://drive.google.com/file/d/1c3hpz90nAbcNdyMFc3pcbnHZUqi-4n6Z/view?usp=sharing
## 🎞Demo Video
https://drive.google.com/file/d/1MzDSEd7gPZIqLVVFc3WQ6Gwguf5WwMRI/view?usp=sharing
## 🖼Frontend
### 🎨Design
  > [Design Document](https://www.notion.so/Design-Document-6c5e22d55a614606bd231c488e26e770)    
  
### 🏠Structure
  > [frontend/src/components](./frontend/src/components) : Directory for components   
  > [frontend/src/font](./frontend/src/font) : Directory for font   
  > [frontend/src/images](./frontend/src/images) : Directory for images   
  > [frontend/src/routes](./frontend/src/routes) : Directory for routes   

<div align="right">
    <b><a href="#2021-Summer-SilliconValley-Internship-Project">⬆️ Back to Top</a></b>
</div>

## ✨Backend
### 🏠Structure
  > [backend](./backend) : Directory for backend   
  > [backend/server.py](./backend/server.py) : Main module   
  > [backend/user.py](./backend/user.py) : Module for user management functions   
  > [backend/record_exercise.py](./backend/record_exercise.py) : Module for kinetic statistical functions   
  > [backend/tts.py](./backend/tts.py) : Module for text-to-speech functions   
  > [backend/search.py](./backend/search.py) : Module for search functions   
  > [backend/Dockerfile](./backend/Dockerfile) : Dockerfile for backend   
  > [frontend/Dockerfile](./frontend/Dockerfile) : Dockerfile for frontend   
  > [nginx](./nginx) : Directory for nginx   
  > [docker-compose.yml](./docker-compose.yml) : Dockerfile Compose for development   
  > [docker-compose-prod.yml](./docker-compose-prod.yml) : Dockerfile Compose for deployment   

<div align="right">
    <b><a href="#2021-Summer-SilliconValley-Internship-Project">⬆️ Back to Top</a></b>
</div>

## 🤖AI
### 🏋️Mediapipe ML solution test
  > [Mediapipe ML solution test](https://www.notion.so/Mediapipe-ML-solution-test-4b08f970dcff40faa20d960bbc6fe161)  

### 🦵Squat 기준
  > [Squat](https://www.notion.so/Squat-c2e93f74fcad42308a095483e64c071e)  

### 💪Push Up 기준
  > [Push Up](https://www.notion.so/Push-Up-7b44a151906c4fd08616a288f7695213) 

### 🏠Structure
  > [backend/cal_pose.py](./backend/cal_pose.py) : Module for calculate pose  
  > [backend/cal_pushup.py](./backend/cal_pushup.py) : Module for count pushup and pushup guide  
  > [backend/cal_squat.py](./backend/cal_squat.py) : Module for count squat and squat guide     



<div align="right">
    <b><a href="#2021-Summer-SilliconValley-Internship-Project">⬆️ Back to Top</a></b>
</div>

## 👩‍👩‍👧‍👧🧑Contributors
| Name | Country | Where to find us | Role |
| ---- | ------- | ----------------- | ---- |
| Yejin Kwon <br /> <img src="https://avatars.githubusercontent.com/yejin0928" width="100" />  | Republic of Korea | [Github](https://github.com/yejin0928)| Backend |
| Sijeong Kim <br /> <img src="https://avatars.githubusercontent.com/Si-jeong" width="100" />  | Republic of Korea | [Github](https://github.com/Si-jeong)| Backend |
| Geonyeol Ryu <br /> <img src="https://avatars.githubusercontent.com/rjsduf0503" width="100" />  | Republic of Korea | [Github](https://github.com/rjsduf0503)| Frontend |
| Yeeun Choi <br /> <img src="https://avatars.githubusercontent.com/swcye" width="100" />  | Republic of Korea | [Github](https://github.com/swcye)| AI |
| Minji Jang <br /> <img src="https://avatars.githubusercontent.com/SUMMERLOVE7" width="100" />  | Republic of Korea | [Github](https://github.com/SUMMERLOVE7)| AI |

<div align="right">
    <b><a href="#2021-Summer-SilliconValley-Internship-Project">⬆️ Back to Top</a></b>
</div>

## 📌Docker Prerequisites

-   Windows [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)
-   Mac [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)

### [](https://github.com/shpark76/docker-demo#1-git-clone)1\. git clone

```
git clone https://github.com/Summer-internship-team-G/hont.git
```

### [](https://github.com/shpark76/docker-demo#2-docker-compose-build-and-up)2\. docker compose build

```
docker-compose build
```

### 3\. docker compose up

```
docker-compose up
```

<div align="right">
    <b><a href="#2021-Summer-SilliconValley-Internship-Project">⬆️ Back to Top</a></b>
</div>
