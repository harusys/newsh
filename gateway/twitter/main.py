from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# 環境設定
URL=os.getenv('NEWSH_TWITTER_URL', None)

class Trend(BaseModel):
    name: str
    tweet_volume: int = None


@app.get("/twitter")
async def call_twitter():
    # Newsh Twitter API 呼び出し
    response = requests.get(URL).json()
    return response