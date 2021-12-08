from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import logging
from typing import Optional

app = FastAPI()

# 環境設定
URL=os.getenv('NEWSH_WEATHER_URL', None)

# class Trend(BaseModel):
#     name: str
#     tweet_volume: int = None


@app.get("/weather")
async def call_twitter():
    # Newsh weather API 呼び出し
    response = requests.get(URL)
    logging.info(f'Return is {response.text}')
    return response.text