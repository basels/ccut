FROM ubuntu:16.04
MAINTAINER Basel Shbita "shbita@usc.edu"

RUN apt-get update -y && apt-get -y upgrade && apt-get install -y python3-pip python3-dev

COPY ./app /app
WORKDIR /app
WORKDIR ccut_lib
RUN pwd

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=main.api

EXPOSE 5000
ENTRYPOINT ["flask"]