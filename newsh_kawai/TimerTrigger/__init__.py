import logging
import datetime
import os
import azure.functions as func

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

user_id = "Uc130132ff505a8a2072da4ec25ca1282"

@handler.add(MessageEvent, message=TextMessage)
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if mytimer.past_due:
        logging.info('The timer is past due!')
        messages = TextSendMessage(text=f"Past_dueが実行されました")
        line_bot_api.push_message(user_id, messages=messages)
    logging.info('The !New! timer is past due!')
    messages = TextSendMessage(text=f"こんにちは!!!\n最近はいかがお過ごしでしょうか?!!!")
    broadmessages = TextSendMessage(text=f"友達のみなさん，hello！")
    line_bot_api.push_message(user_id, messages=messages)
    line_bot_api.broadcast(messages=broadmessages)
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
