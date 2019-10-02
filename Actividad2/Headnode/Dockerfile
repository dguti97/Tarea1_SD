FROM ubuntu:latest
RUN apt-get update \
	&& apt-get -y install python3 \
	&& apt-get install -y iputils-ping
COPY Headnode.py /Headnode/

WORKDIR /Headnode/
