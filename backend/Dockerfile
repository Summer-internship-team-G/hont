# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /server
COPY server.py ./

EXPOSE 5000

CMD python server.py

# FROM python:3.6-slim

# #RUN apk --no-cache add --virtual .builddeps gcc gfortran musl-dev     && pip install numpy==1.14.0    && apk del .builddeps     && rm -rf /root/.cache

# WORKDIR /server
# # Install python dependencies
# RUN pip install --upgrade pip
# RUN apt-get update 
# RUN apt-get -y install libgl1-mesa-glx
# RUN apt-get -y install libglib2.0-0


# COPY requirements.txt ./

# RUN pip install -r requirements.txt

# COPY server.py ./

# EXPOSE 5000

# CMD python server.py