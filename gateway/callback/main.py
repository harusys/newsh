import os
from typing import List, Optional

from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI, Header, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from pydantic import BaseModel

from ..timer import get_twitter_trends

app = FastAPI()

# 環境設定
TWITTER_TREND_KEYWORD = os.environ["TWITTER_TREND_KEYWORD"]
WEATHER_KEYWORD = os.environ["WEATHER_KEYWORD"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential,
    )
    # シークレットを直接取得
    LINE_CHANNEL_ACCESS_TOKEN = client.get_secret(
        "LINE-CHANNEL-ACCESS-TOKEN"
    ).value
    LINE_CHANNEL_SECRET = client.get_secret("LINE-CHANNEL-SECRET").value

# インスタンス生成
handler = WebhookHandler(LINE_CHANNEL_SECRET)
line = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


class Line(BaseModel):
    destination: str
    events: List[Optional[None]]


@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):

    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(
            status_code=400, detail="chatbot handle body error."
        )
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

    if event.message.text == TWITTER_TREND_KEYWORD:
        trends = get_twitter_trends()
        line.reply_message(event.reply_token, TextSendMessage(text=trends))

    if event.message.text == WEATHER_KEYWORD:
        line.reply_message(
            event.reply_token, TextSendMessage(text="リリースまでお待ち下さい。")
        )

    else:
        line.reply_message(
            event.reply_token, TextSendMessage(text="すみません、\nよく分かりませんでした。")
        )
