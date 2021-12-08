import azure.functions as func
from bonnette import Bonnette
import os
import logging

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

# # Azure FunctionsのApplication Settingに設定した値から取得する↓
# channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# line_bot_api = LineBotApi(channel_access_token)
# handler = WebhookHandler(channel_secret)

# @handler.add(MessageEvent, message=TextMessage)
# def main(req: func.HttpRequest, event) -> func.HttpResponse:
#     handler = Bonnette(app)
#     logging.info(f'FINAL Return is {handler(req)}')
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=f'{handler(req)}')
#     )


def main(req: func.HttpRequest) -> func.HttpResponse:
    handler = Bonnette(app)
    logging.info(f'FINAL Return is {handler(req)}')
    return handler(req)