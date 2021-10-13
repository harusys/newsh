import logging
import os
import azure.functions as func
import requests
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# Azure FunctionsのApplication Settingに設定した値から取得する↓
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)




def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get x-line-signature header value
    signature = req.headers['x-line-signature']

    # get request body as text
    body = req.get_body().decode("utf-8")
    logging.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        func.HttpResponse(status_code=400)

    return func.HttpResponse('OK')


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    logging.info('aaaaaaaaaaaaaaaaaaaaaa.')

    profile = line_bot_api.get_profile(event.source.user_id)
    profile.display_name #-> 表示名
    profile.user_id #-> ユーザーID

    url = "https://weather.tsukumijima.net/api/forecast?city=140010"
    r = requests.get(url)
    jsonData = r.json()
    w = jsonData["forecasts"][0]["telop"]
    # dateday = r.response.data.forecasts[0].date
    logging.info(jsonData)
    logging.info(w)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=profile.display_name + 'さんこんにちは．あなたが打ったのは「' + event.message.text + '」です．ユーザIDは「' + profile.user_id + '」です．天気は'+w+'です')
        
    )