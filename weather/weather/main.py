from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
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
# OpenWeatherAPI
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
BASE_URL = os.getenv('OPEN_WEATHER_API_BASE_URL')
city = os.getenv('CITY_NAME')
# ToDo：LINEから都市を指定
#city = event.message.text

# ローカル実行時は Key Vault 参照機能不可
if os.getenv("Environment") == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-prod-je-001.vault.azure.net",
        credential=credential)
    # シークレットを直接取得
    API_KEY = client.get_secret("OPEN-WEATHER-API-KEY").value

# To Do : クラス設定
# モデルで必要な情報を絞り込み
class Weather(BaseModel):
    weather: str
    tweet_volume: int = None

@app.get("/weather")
async def weather_get():

    # トレンドを取得
    response = requests.get(f'{BASE_URL}?q={city}&units=metric&lang=ja&APPID={API_KEY}')
    forecastData = json.loads(response.text)
    
    for item in forecastData['list']:
        #To Do : 日本語変換したい
        #forecastDatetime = datetime.fromtimestamp(item["dt"])
        # forecastDatetime = (item["dt"])
        #forecastDatetime = forecastDatetime24.astimezone(timezone('Asia/Tokyo'))
        #forecastDatetime = timezone('Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))
        weatherDescription = item['weather'][0]['description']
        temperature = item['main']['temp']
        rainfall = 0
        if 'rain' in item and '3h' in item['rain']:
            rainfall = item['rain']['3h']

    weatherList = {}
    weatherList["WeatherDescription"] = weatherDescription
    weatherList["Temperature"] = temperature
    weatherList["Rainfall"] = rainfall

    logging.info(f'Return of main is{weatherList}')

    # 応答
    return weatherList
