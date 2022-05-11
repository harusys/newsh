import json
import logging
import os
from typing import List

import requests
from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI
from pydantic import BaseModel, parse_obj_as

app = FastAPI()

# 環境設定
# OpenWeatherAPI
API_KEY = os.environ["OPEN_WEATHER_API_KEY"]
BASE_URL = os.environ["OPEN_WEATHER_API_BASE_URL"]
city = os.environ["CITY_NAME"]
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
class Weather(BaseModel):
    weather_description: str
    temperature: float
    rainfall: float


class WeatherGet2(BaseModel):
    weather_description: str
    temperature: float
    rainfall: float


class WeatherGet(BaseModel):
    weather_description: WeatherGet2
    temperature: float
    rainfall: float


@app.get("/weather", response_model=List[Weather])
async def weather_get():

    # 天気情報を取得
    response = requests.get(
        f"{BASE_URL}?q={city}&units=metric&lang=ja&APPID={API_KEY}"
    )
    forecastData = json.loads(response.text)
    forecastData_items = parse_obj_as(List[Weather], forecastData)

    # TODO: 複数の時間での天気情報取得
    weatherDescription = forecastData_items[-1].weather_description
    temperature = forecastData_items[-1]["main"]["temp"]
    rainfall = 0
    if (
        "rain" in forecastData_items[-1]
        and "3h" in forecastData_items[-1]["rain"]
    ):
        rainfall = forecastData_items[-1]["rain"]["3h"]

    weatherList = {}
    weatherList["WeatherDescription"] = weatherDescription
    weatherList["Temperature"] = temperature
    weatherList["Rainfall"] = rainfall

    logging.info(f"Return of main is{weatherList}")

    # 応答
    return weatherList
