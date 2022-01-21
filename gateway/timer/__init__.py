import os
from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import List

import azure.functions as func
import requests
from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from linebot import LineBotApi
from linebot.models import TextSendMessage
from pydantic import parse_obj_as

from .cosmosdb import DbConnection
from .models.teitter_trend import TwitterTrend

# 環境設定
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_PRIMARYKEY = os.environ["COSMOS_PRIMARYKEY"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
TWITTER_TREND_URL = os.environ["TWITTER_TREND_URL"]
TWITTER_TREND_HIGHER_THAN = os.environ["TWITTER_TREND_HIGHER_THAN"]

# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential,
    )
    # シークレットを直接取得
    COSMOS_ENDPOINT = client.get_secret("COSMOS-ENDPOINT").value
    COSMOS_PRIMARYKEY = client.get_secret("COSMOS-PRIMARYKEY").value
    LINE_CHANNEL_ACCESS_TOKEN = client.get_secret(
        "LINE-CHANNEL-ACCESS-TOKEN"
    ).value

# インスタンス生成
line = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
logger = getLogger(__name__)


def main(mytimer: func.TimerRequest) -> None:

    # スケジュール遅延確認
    if mytimer.past_due:
        logger.info("The timer is past due!")

    # 日時取得
    JST = timezone(timedelta(hours=+9), "JST")
    jst_timestamp = datetime.now(JST)

    logger.info(
        "Python timer trigger function ran at %s", jst_timestamp.isoformat()
    )

    # Cosmos DB からタイマー情報を取得
    dbConn = DbConnection(COSMOS_ENDPOINT, COSMOS_PRIMARYKEY)
    timers = dbConn.timer_manager().find_by_time(jst_timestamp)

    for timer in timers:
        if timer.task_name == "twitter":
            # Twitter トレンド取得
            trends = get_twitter_trends()

            # LINE 通知
            # ユーザ毎のレコード登録が必要なため、現時点はブロードキャストで通知
            # line.push_message(timer.user_id, TextSendMessage(text=trends))
            # logger.info(
            #     "Twitter push message is completed to {0}", timer.user_id
            # )
            line.broadcast(TextSendMessage(text=trends))

    # タイマー起動のため応答なし


def get_twitter_trends():

    # 日時取得
    JST = timezone(timedelta(hours=+9), "JST")
    jst_timestamp = datetime.now(JST)

    logger.info(
        "Python timer trigger function ran at %s", jst_timestamp.isoformat()
    )

    # Newsh Twitter API (trends) 呼び出し
    response = requests.get(TWITTER_TREND_URL).json()
    trends = parse_obj_as(List[TwitterTrend], response)

    # LINE 通知用にメッセージ整形
    msg_header = "Twitter 日本のトレンド\n"
    msg_header += f"{jst_timestamp.strftime('%Y年%m月%d日 %H:%M:%S')} 時点\n"
    msg_body = ""

    for i in range(int(TWITTER_TREND_HIGHER_THAN)):
        msg_body += f"\n{i+1}. {trends[i].name}"

    return msg_header + msg_body
