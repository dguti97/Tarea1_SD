FROM ubuntu:latest
RUN apt-get update \
	&& apt-get -y install python3 \
	&& apt-get install -y iputils-ping

COPY datanode2.py /Datanode2/

WORKDIR /Datanode2/
