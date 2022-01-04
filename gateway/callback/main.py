from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
from pydantic import BaseModel, parse_obj_as
from typing import List, Optional
import os
import requests

app = FastAPI()

# 環境設定
TWITTER_TREND_URL = os.environ["TWITTER_TREND_URL"]
TWITTER_TREND_KEYWORD = os.environ["TWITTER_TREND_KEYWORD"]
TWITTER_TREND_HIGHER_THAN = os.environ["TWITTER_TREND_HIGHER_THAN"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]


# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential)
    # シークレットを直接取得
    LINE_CHANNEL_ACCESS_TOKEN = client.get_secret(
        "LINE-CHANNEL-ACCESS-TOKEN").value
    LINE_CHANNEL_SECRET = client.get_secret(
        "LINE-CHANNEL-SECRET").value


# モデルで必要な情報を絞り込み
class Trend(BaseModel):
    name: str
    tweet_volume: int = None


@app.post("/callback")
async def callback(request: Request):
    
    parser = WebhookParser(channel_secret=LINE_CHANNEL_SECRET)

    # リクエストをパースしてイベントを取得（署名の検証あり）
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""))

    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

    # 各イベントを処理
    for ev in events:
        await line_bot_api.reply_message(
            ev.reply_token,
            TextMessage(text=f"You said: {ev.message.text}"))

    # LINEサーバへHTTP応答を返す
    return "ok"

    # Newsh Twitter API (trends) 呼び出し
    # response = requests.get(TWITTER_TREND_URL).json()
    # trends = parse_obj_as(List[Trend], response)

    # # LINE 通知用にメッセージ整形
    # msg_header = f"Twitter 日本のトレンド\n"
    # msg_header += f"{jst_timestamp.strftime('%Y年%m月%d日 %H:%M:%S')} 時点\n"
    # msg_body = ""

    # for i in range(int(TWITTER_TREND_HIGHER_THAN)):
    #     msg_body += f"\n{i+1}. {trends[i].name}"

    # # LINE 通知
    # line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    # line_bot_api.reply_message(eve TextSendMessage(text=msg_header + msg_body))

    # # 応答
    # return "ok"
