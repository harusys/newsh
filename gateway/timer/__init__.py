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

# 環境設定（Azure FunctionsのApplication Settingに設定した値から取得する）
URL = os.getenv("NEWSH_WEATHER_URL")
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def main(mytimer: func.TimerRequest) -> None:
    # スケジュール遅延確認
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info(f'Start2')

    # Newsh weather API 呼び出し
    logging.info(URL)
    logging.info(channel_secret)
    response = requests.get(URL).json()
    # response = requests.get("https://func-newsh-weather-prod-japaneast-001.azurewebsites.net/weather?code=4buZaDvSUaYB7jXpWkM9laPV8g8dEkb9k1xv8k4nu/Hqnt0KuXXw8w==").json()

    responseText = f'天気：{response["WeatherDescription"]}\n'
    responseText += f'気温：{response["Temperature"]} ℃\n'
    responseText += f'降水確率：{response["Rainfall"]} mm'
    logging.info(f'Return is {responseText}')

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
