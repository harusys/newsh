# Find the Dockerfile for mcr.microsoft.com/azure-functions/python:3.0-python3.8-core-tools at this URL
# https://github.com/Azure/azure-functions-docker/blob/dev/host/3.0/buster/amd64/python/python38/python38-core-tools.Dockerfile
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-core-tools

#RUN pip install fastapi uvicorn[standard]
RUN pip install azure-functions bonnette fastapi

#RUN pip install other module for Newsh
RUN pip install tweepy line-bot-sdk azure-identity azure-keyvault-secrets flake8