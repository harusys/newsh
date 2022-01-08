import azure.functions as func
from bonnette import Bonnette
import os
import logging
import requests
from datetime import datetime, timedelta, timezone

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from .main import app

URL=os.getenv('NEWSH_WEATHER_URL')

# Azure FunctionsのApplication Settingに設定した値から取得する↓
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# @handler.add(MessageEvent, message=TextMessage)
# def main(req: func.HttpRequest, event) -> func.HttpResponse:
#     handler = Bonnette(app)
#     logging.info(f'FINAL Return is {handler(req)}')
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=f'{handler(req)}')
#     )

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info(f'Start')
#     handler = Bonnette(app)
#     logging.info(handler(req))
#     logging.info(f'FINAL Return is {handler(req)}')
#     logging.info(f'Stop')
#     return handler(req)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Start2')
    # Newsh weather API 呼び出し
    # response = requests.get(URL).json()
    response = requests.get('https://func-newsh-weather-prod-japaneast-001.azurewebsites.net/weather?code=oXiIlbUcEkqlz2W1bejM2Imy3abiWyziRWfs/PrsyZFx3uRv4IFjhg==').json()
    # logging.info(f'Return is {response.text}')
    logging.info(f'Return is {response}')

    responseText = f'天気：{response["WeatherDescription"]}\n'
    responseText += f'気温：{response["Temperature"]} ℃\n'
    responseText += f'降水確率：{response["Rainfall"]} mm'
    logging.info(f'Return is {responseText}')
    # return responseText

    # 日時取得
    JST = timezone(timedelta(hours=+9), 'JST')
    jst_timestamp = datetime.now(JST)

     # LINE 通知用にメッセージ整形
    msg_header = f"weather 横浜の天気\n"
    msg_header += f"{jst_timestamp.strftime('%Y年%m月%d日 %H:%M:%S')} 時点\n"
    msg_body = responseText

    # LINE 通知
    line_bot_api = LineBotApi(channel_access_token)
    # line_bot_api.reply_message(TextSendMessage(text=msg_header + msg_body))
    line_bot_api.broadcast(TextSendMessage(text=msg_header + msg_body))