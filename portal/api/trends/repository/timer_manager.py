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
        self.container = database.get_container_client("TIMER_MANAGER")

    def find_by_userid(self, user_id: string) -> List[TimerManager]:
        """ユーザ ID 指定で検索"""
        try:
            items = list(
                self.container.read_item(item=user_id, partition_key=user_id)
                # self.container.query_items(
                #     query="SELECT"
                #     + " c.user_id, c.task_name, c.scheduled_at"
                #     + " FROM c"
                #     + " WHERE c.user_id = @user_id",
                #     parameters=[
                #         {"name": "@user_id", "value": user_id},
                #     ],
                #     # パーティションまたぎ検索は NG
                #     enable_cross_partition_query=False,
                # )
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
        """データ登録"""
        try:
            self.container.create_item(item)

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
            self.container.replace_item(item)

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

    def delete(self, user_id: string) -> None:
        """データ更新"""
        try:
            self.container.delete_item(user_id)

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
