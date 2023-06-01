#!/bin/bash
shopt -s expand_aliases
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 592110663504.dkr.ecr.us-east-1.amazonaws.com
docker build -t trip-to-trivia:latest . 
docker tag trip-to-trivia:latest 592110663504.dkr.ecr.us-east-1.amazonaws.com/trip-to-trivia:latest
docker push 592110663504.dkr.ecr.us-east-1.amazonaws.com/trip-to-trivia