FROM ubuntu:20.04

RUN apt update

RUN apt install -y nano curl unzip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

RUN unzip awscliv2.zip

RUN ./aws/install

RUN curl -o- -L https://slss.io/install | bash

RUN apt install -y nodejs npm