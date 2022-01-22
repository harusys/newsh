import json
import logging
import os
from typing import List

import requests
from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 環境設定
# OpenWeatherAPI
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
BASE_URL = os.getenv("OPEN_WEATHER_API_BASE_URL")
city = os.getenv("CITY_NAME")
# TODO:LINEから都市を指定
# city = event.message.text

# ローカル実行時は Key Vault 参照機能不可
if os.getenv("Environment") == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-prod-je-001.vault.azure.net",
        credential=credential,
    )
    # シークレットを直接取得
    API_KEY = client.get_secret("OPEN-WEATHER-API-KEY").value

# TODO:クラス設定
# モデルで必要な情報を絞り込み
class Weather(BaseModel):
    weather: str


@app.get("/weather", response_model=List[Weather])
async def weather_get():

    # トレンドを取得
    response = requests.get(
        f"{BASE_URL}?q={city}&units=metric&lang=ja&APPID={API_KEY}"
    )
    forecastData = json.loads(response.text)

    for item in forecastData["list"]:
        # TODO: 複数の時間での天気情報取得
        weatherDescription = item["weather"][0]["description"]
        temperature = item["main"]["temp"]
        rainfall = 0
        if "rain" in item and "3h" in item["rain"]:
            rainfall = item["rain"]["3h"]

    weatherList = {}
    weatherList["WeatherDescription"] = weatherDescription
    weatherList["Temperature"] = temperature
    weatherList["Rainfall"] = rainfall

    logging.info(f"Return of main is{weatherList}")

    # 応答
    return weatherList
