#!/bin/bash
shopt -s expand_aliases
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ECR
docker build -t trip-to-trivia:latest . 
docker tag trip-to-trivia:latest $AWS_ECR/trip-to-trivia:latest
docker push $AWS_ECR/trip-to-trivia