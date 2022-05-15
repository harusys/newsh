import json
import logging
import os

# from datetime import date
from typing import List

import requests

# from azure.identity import VisualStudioCodeCredential
# from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI

# from gateway.timer import main
from pydantic import BaseModel, parse_obj_as

app = FastAPI()

# 環境設定
# OpenWeatherAPI
API_KEY = os.environ["OPEN_WEATHER_API_KEY"]
BASE_URL = os.environ["OPEN_WEATHER_API_BASE_URL"]
city = os.environ["CITY_NAME"]
# city = event.message.text

# ローカル実行時は Key Vault 参照機能不可
# if os.environ["Environment"] == "local":
#     credential = VisualStudioCodeCredential()
#     client = SecretClient(
#         vault_url="https://kv-newsh-test-je-001.vault.azure.net",
#         credential=credential,
#     )
#     # シークレットを直接取得
#     API_KEY = client.get_secret("OPEN-WEATHER-API-KEY").value


# モデルで必要な情報を絞り込み


class WeatherList(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class MainList(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: int
    grnd_level: int
    humidity: int
    temp_kf: float


# class RainList(BaseModel):
#     3h: float


class Weather(BaseModel):
    dt: int
    weather: List[WeatherList]
    main: MainList
    visibility: int
    wind: dict
    clouds: dict
    dt: int
    sys: dict
    dt_txt: str
    rain: dict = None
    pop: int


class WeatherResponse(BaseModel):
    WeatherDescription: str
    Temperature: float
    MaxTemperature: float
    MinTemperature: float


@app.get("/weather", response_model=List[WeatherResponse])
async def weather_get():

    # 天気情報を取得
    response = requests.get(
        f"{BASE_URL}?q={city}&units=metric&lang=ja&APPID={API_KEY}"
    )
    forecastData = json.loads(response.text)["list"]
    forecastData_items = parse_obj_as(List[Weather], forecastData)

    # TODO: 複数の時間での天気情報取得
    weatherDescription = forecastData_items[-1].weather[-1].description
    temperature_now = forecastData_items[-1].main.temp
    temperature_max = forecastData_items[-1].main.temp_max
    temperature_min = forecastData_items[-1].main.temp_min

    weatherDict = {}
    weatherDict["WeatherDescription"] = weatherDescription
    weatherDict["Temperature"] = temperature_now
    weatherDict["MaxTemperature"] = temperature_max
    weatherDict["MinTemperature"] = temperature_min

    weatherList = []
    weatherList.append(weatherDict)
    logging.info(f"#############################{weatherList}")

    # 応答
    return weatherList
