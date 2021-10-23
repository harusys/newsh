from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import tweepy
import os

app = FastAPI()


# 環境設定
API_KEY=os.getenv('TWITTER_API_KEY', None)
API_SECRET=os.getenv('TWITTER_API_SECRET', None)
AT_KEY=os.getenv('TWITTER_ACCESS_TOKEN_KEY', None)
AT_SECRET=os.getenv('TWITTER_ACCESS_TOKEN_SECRET', None)

WID = 23424856 # 日本


# モデルで必要な情報を絞り込み
class Trend(BaseModel):
    name: str
    tweet_volume: int = None


@app.get("/trends", response_model=List[Trend])
async def twitter_trends():

    # 認証情報をセット
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(AT_KEY, AT_SECRET)

    # トレンドを取得
    api = tweepy.API(auth)
    response = api.get_place_trends(WID)[0]

    # 応答
    return response["trends"]
