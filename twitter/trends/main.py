from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import tweepy

app = FastAPI()

# 環境設定
API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
AT_KEY = os.environ["TWITTER_ACCESS_TOKEN_KEY"]
AT_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential)
    # シークレットを直接取得
    API_KEY = client.get_secret("TWITTER-API-KEY").value
    API_SECRET = client.get_secret("TWITTER-API-SECRET").value
    AT_KEY = client.get_secret("TWITTER-ACCESS-TOKEN-KEY").value
    AT_SECRET = client.get_secret("TWITTER-ACCESS-TOKEN-SECRET").value

WID = 23424856  # 日本


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
