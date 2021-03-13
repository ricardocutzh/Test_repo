#!/bin/bash
echo "executing shell script"

sudo yum update -y

sudo amazon-linux-extras install ansible2 -y

sudo amazon-linux-extras install docker -y

sudo usermod -a -G docker ec2-user

sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose