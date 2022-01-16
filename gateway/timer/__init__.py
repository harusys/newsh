from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from datetime import datetime, timedelta, timezone
from linebot import LineBotApi
from linebot.models import TextSendMessage
from pydantic import BaseModel, parse_obj_as
from typing import List
import azure.functions as func
import os
import requests
import logging

# 環境設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
TWITTER_TREND_URL = os.environ["TWITTER_TREND_URL"]
TWITTER_TREND_HIGHER_THAN = os.environ["TWITTER_TREND_HIGHER_THAN"]

# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential)
    # シークレットを直接取得
    LINE_CHANNEL_ACCESS_TOKEN = client.get_secret(
        "LINE-CHANNEL-ACCESS-TOKEN").value

# インスタンス生成
line = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


class Trend(BaseModel):
    name: str
    tweet_volume: int = None


def main(mytimer: func.TimerRequest) -> None:

    # スケジュール遅延確認
    if mytimer.past_due:
        logging.info('The timer is past due!')

    # Twitter トレンド取得
    trends = get_twitter_trends()

    # LINE 通知
    line.broadcast(TextSendMessage(text=trends))

    # タイマー起動のため応答なし


def get_twitter_trends():

    # 日時取得
    JST = timezone(timedelta(hours=+9), 'JST')
    jst_timestamp = datetime.now(JST)

    logging.info('Python timer trigger function ran at %s',
                 jst_timestamp.isoformat())

    # Newsh Twitter API (trends) 呼び出し
    response = requests.get(TWITTER_TREND_URL).json()
    trends = parse_obj_as(List[Trend], response)

    # LINE 通知用にメッセージ整形
    msg_header = f"Twitter 日本のトレンド\n"
    msg_header += f"{jst_timestamp.strftime('%Y年%m月%d日 %H:%M:%S')} 時点\n"
    msg_body = ""

    for i in range(int(TWITTER_TREND_HIGHER_THAN)):
        msg_body += f"\n{i+1}. {trends[i].name}"

    return msg_header + msg_body
