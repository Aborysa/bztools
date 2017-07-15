FROM ubuntu:latest
MAINTAINER Mario
RUN apt-get update
RUN apk add --update make tar unzip gcc openssl-dev readline-dev curl libc-dev
RUN apt-get install -y zip
RUN apt-get install -y rsync
RUN apt-get install -y python3
RUN apt-get install -y lua5.2
RUN apt-get install -y luarocks
ADD ./pytools /bztools