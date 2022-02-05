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
API_KEY = os.environ["OPEN_WEATHER_API_KEY"]
BASE_URL = os.environ["OPEN_WEATHER_API_BASE_URL"]
city = os.environ["CITY_NAME"]
# TODO:LINEから都市を指定
# city = event.message.text

# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential,
    )
    # シークレットを直接取得
    API_KEY = client.get_secret("OPEN-WEATHER-API-KEY").value


# モデルで必要な情報を絞り込み
# TODO:クラス設定
class Weather(BaseModel):
    weather: dict


@app.get("/weather", response_model=List[Weather])
async def weather_get():

    # トレンドを取得
    response = requests.get(
        f"{BASE_URL}?q={city}&units=metric&lang=ja&APPID={API_KEY}"
    )
    forecastData = json.loads(response.text)

    # TODO: 複数の時間での天気情報取得
    weatherDescription = forecastData[-1]["weather"][0]["description"]
    temperature = forecastData[-1]["main"]["temp"]
    rainfall = 0
    if "rain" in forecastData[-1] and "3h" in forecastData[-1]["rain"]:
        rainfall = forecastData[-1]["rain"]["3h"]

    weatherList = {}
    weatherList["WeatherDescription"] = weatherDescription
    weatherList["Temperature"] = temperature
    weatherList["Rainfall"] = rainfall

    logging.info(f"Return of main is{weatherList}")

    # 応答
    return weatherList
