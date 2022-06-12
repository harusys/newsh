# Find the Dockerfile for mcr.microsoft.com/azure-functions/python:3.0-python3.8-core-tools at this URL
# https://github.com/Azure/azure-functions-docker/blob/dev/host/3.0/buster/amd64/python/python38/python38-core-tools.Dockerfile
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-core-tools

# For Fast API
RUN pip install azure-functions bonnette fastapi tweepy

# For Linter / Formatter
RUN pip install flake8 black

# For other module Newsh
RUN pip install line-bot-sdk azure-identity azure-keyvault-secrets
