FROM ubuntu:latest
RUN apt-get update \
	&& apt-get -y install python3 \
	&& apt-get install -y iputils-ping

COPY datanode3.py /Datanode3/

WORKDIR /Datanode3/
