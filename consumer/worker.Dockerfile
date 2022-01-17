# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
COPY ./pip/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./src/ .
RUN rm main.py
RUN rm requirements.txt