FROM ubuntu:latest

RUN apt-get update \
	&& apt-get -y install python3

COPY server.py /appserver/

WORKDIR /appserver/
