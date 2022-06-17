# Find the Dockerfile for mcr.microsoft.com/azure-functions/python:3.0-python3.8-core-tools at this URL
# https://github.com/Azure/azure-functions-docker/blob/dev/host/3.0/buster/amd64/python/python38/python38-core-tools.Dockerfile
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-core-tools

# For Linter / Formatter
RUN pip install flake8 black

# For React
ENV NODE_VERSION=16
RUN \
    apt-get update \
    && curl -fsSL https://deb.nodesource.com/setup_$NODE_VERSION.x | sudo -E bash - \
    && apt-get install nodejs -y \
    && apt-get install yarn -y