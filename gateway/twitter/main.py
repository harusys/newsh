from fastapi import FastAPI
from pydantic import BaseModel

import requests
import os

app = FastAPI()

# 環境設定
URL = os.getenv('NEWSH_TWITTER_URL', None)


class Trend(BaseModel):
    name: str
    tweet_volume: int = None


@app.get("/twitter/trends")
async def call_twitter_trends():
    # Newsh Twitter API (trends) 呼び出し
    response = requests.get(URL).json()

    return response