from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import logging
from typing import Optional

app = FastAPI()

# 環境設定
# URL=os.getenv('NEWSH_WEATHER_URL', None)
URL=os.getenv('NEWSH_WEATHER_URL')

# class Trend(BaseModel):
#     name: str
#     tweet_volume: int = None

@app.get("/")
async def call_weather():
    logging.info(f'Start1')
    # Newsh weather API 呼び出し
    response = requests.get(URL)
    logging.info(f'Return is {response.text}')
    return response.text

@app.get("/Weather2")
async def call_weather():
    logging.info(f'Start2')
    # Newsh weather API 呼び出し
    # response = requests.get(URL)
    response = requests.get('https://func-newsh-weather-prod-japaneast-001.azurewebsites.net/weather?code=oXiIlbUcEkqlz2W1bejM2Imy3abiWyziRWfs/PrsyZFx3uRv4IFjhg==')
    logging.info(f'Return is {response.text}')
    return response.text