from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI
from linebot import LineBotApi
from linebot.models import TextSendMessage
from pydantic import BaseModel, parse_obj_as
from typing import List
import datetime
import os
import requests

app = FastAPI()

# 環境設定
URL = os.environ["NEWSH_TWITTER_URL"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential)
    # シークレットを直接取得
    LINE_CHANNEL_ACCESS_TOKEN = client.get_secret(
        "LINE-CHANNEL-ACCESS-TOKEN").value


class Trend(BaseModel):
    name: str
    tweet_volume: int = None


@app.get("/twitter/trends")
async def call_twitter_trends():

    # Newsh Twitter API (trends) 呼び出し
    response = requests.get(URL).json()
    trends = parse_obj_as(List[Trend], response)

    # LINE 通知用にメッセージ整形
    msg_header = f"Twitter 日本のトレンド\n{datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')} 時点\n"
    msg_body = ""

    for i, trend in enumerate(trends):
        msg_body += f"\n{i+1}. {trend.name}"

    # LINE 通知
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text=msg_header + msg_body))

    # 応答
    return "LINE Notification Completed."
