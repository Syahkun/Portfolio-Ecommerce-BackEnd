#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
docker stop backend
docker rm backend
docker rmi syahkun/flask-tutorial:latest
docker run -d --name flask-tutorial -p 5000:5000 syahkun/flask-tutorial:latest