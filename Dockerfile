FROM ubuntu:20.04

RUN apt update

RUN apt install -y zip

RUN apt install -y unzip

RUN apt install -y curl

RUN apt install -y nano 