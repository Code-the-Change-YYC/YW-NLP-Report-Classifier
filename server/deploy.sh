#!/bin/bash

# This script assumes that the required AWS permissions are set up in the CLI. 
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 847668204885.dkr.ecr.us-west-2.amazonaws.com

docker build -t nlp-prototype-client-local client
docker tag nlp-prototype-client-local:latest 847668204885.dkr.ecr.us-west-2.amazonaws.com/nlp-prototype-client-local:latest
docker push 847668204885.dkr.ecr.us-west-2.amazonaws.com/nlp-prototype-client-local:latest

docker build -t nlp-prototype-server .
docker tag nlp-prototype-server:latest 847668204885.dkr.ecr.us-west-2.amazonaws.com/nlp-prototype-server:latest
docker push 847668204885.dkr.ecr.us-west-2.amazonaws.com/nlp-prototype-server:latest