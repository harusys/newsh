import os
import string
from logging import getLogger
from typing import List

from azure.cosmos import DatabaseProxy, exceptions
from pydantic import parse_obj_as

from ..models.timer_manager import TimerManager

logger = getLogger(__name__)


class TimerManagerRepository:
    """タイマ管理コンテナ用クラス"""

    def __init__(self, database: DatabaseProxy) -> None:
        self.container = database.get_container_client(
            os.environ["COSMOS_CONTAINER_TIMER_MANAGER"]
        )

    def find_by_userid(self, user_id: str) -> List[TimerManager]:
        """ユーザ ID 指定で検索"""
        try:
            items = list(
                self.container.query_items(
                    query="SELECT"
                    + " c.id, c.user_id, c.task_name, c.scheduled_at"
                    + " FROM c"
                    + " WHERE c.user_id = @user_id",
                    parameters=[
                        {"name": "@user_id", "value": user_id},
                    ],
                    # パーティションまたぎ検索は NG
                    enable_cross_partition_query=False,
                )
            )
            # RU は課金に跳ねるためチェック用にログ出力
            request_charge = (
                self.container.client_connection.last_response_headers[
                    "x-ms-request-charge"
                ]
            )

            logger.info("Query returned {0} items.".format(len(items)))
            logger.info(
                "Operation consumed {0} request units".format(request_charge)
            )
            return parse_obj_as(List[TimerManager], items)

        except exceptions.CosmosHttpResponseError as failure:
            logger.error(
                "Failed to select timer manager. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure

    def create(self, item: TimerManager) -> None:
        """スケジュール登録"""
        try:
            logger.info("Inserting item {0}".format(item))
            self.container.create_item(item.dict())

            # RU は課金に跳ねるためチェック用にログ出力
            request_charge = (
                self.container.client_connection.last_response_headers[
                    "x-ms-request-charge"
                ]
            )

            logger.info(
                "Operation consumed {0} request units".format(request_charge)
            )
            return None

        except exceptions.CosmosHttpResponseError as failure:
            logger.error(
                "Failed to create timer manager. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure

    def update(self, item: TimerManager) -> None:
        """データ更新"""
        try:
            # 更新対象を id 検索で取得
            read_item = self.container.read_item(
                item=item.id, partition_key=item.user_id
            )
            # データ置換
            self.container.replace_item(item=read_item, body=item.dict())

            # RU は課金に跳ねるためチェック用にログ出力
            request_charge = (
                self.container.client_connection.last_response_headers[
                    "x-ms-request-charge"
                ]
            )

            logger.info(
                "Operation consumed {0} request units".format(request_charge)
            )
            return None

        except exceptions.CosmosHttpResponseError as failure:
            logger.error(
                "Failed to update timer manager. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure

    def delete(self, item: TimerManager) -> None:
        """データ削除"""
        try:
            self.container.delete_item(
                item=item.id, partition_key=item.user_id
            )

            # RU は課金に跳ねるためチェック用にログ出力
            request_charge = (
                self.container.client_connection.last_response_headers[
                    "x-ms-request-charge"
                ]
            )

            logger.info(
                "Operation consumed {0} request units".format(request_charge)
            )
            return None

        except exceptions.CosmosHttpResponseError as failure:
            logger.error(
                "Failed to delete timer manager. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure
