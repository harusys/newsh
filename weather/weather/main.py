from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import logging
import requests
import os
import json
import datetime

app = FastAPI()


# 環境設定


# モデルで必要な情報を絞り込み
# class Trend(BaseModel):
#     name: str
#     tweet_volume: int = None


@app.get("/weather")
async def weather_get():

    # OpenWeatherAPI
    API_KEY = "3acade7963ee118c50ddc8fbff4a2e64"
    BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
    city = "yokohama"
    #city = event.message.text
    response = requests.get(f'{BASE_URL}?q={city}&units=metric&lang=ja&APPID={API_KEY}')
    forecastData = json.loads(response.text)

    # トレンドを取得
    for item in forecastData['list']:
        #forecastDatetime = datetime.fromtimestamp(item["dt"])
        forecastDatetime = (item["dt"])
        #logging.info(forecastDatetime)
        #To Do : 日本語変換したい
        #forecastDatetime = forecastDatetime24.astimezone(timezone('Asia/Tokyo'))
        #forecastDatetime = timezone('Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))
        #logging.info(forecastDatetime)
        weatherDescription = item['weather'][0]['description']
        temperature = item['main']['temp']
        rainfall = 0
        if 'rain' in item and '3h' in item['rain']:
            rainfall = item['rain']['3h']
        # print('日時:{0} 天気:{1} 気温(℃):{2} 雨量(mm):{3}'.format(
        #     forecastDatetime, weatherDescription, temperature, rainfall))

    responseText = f'今日の天気は{forecastDatetime}, {weatherDescription}, {temperature}, {rainfall}です'
    
    # responseText = f'abcd'
    # logging.info(f'Return of main is{responseText}')
    # 応答
    return responseText
