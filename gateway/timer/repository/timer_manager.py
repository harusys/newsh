from datetime import time
from faulthandler import is_enabled
from logging import getLogger
from typing import List

from azure.cosmos import DatabaseProxy, exceptions
from pydantic import BaseModel, parse_obj_as

logger = getLogger(__name__)


class TimerManager(BaseModel):
    user_id: str
    task_name: str
    scheduled: time
    is_enabled: bool


class TimerManagerRepository:
    """タイマ管理コンテナ用クラス"""

    def __init__(self, database: DatabaseProxy) -> None:
        self.container = database.get_container_client("task_manager")

    def read_all_items(self) -> List[TimerManager]:
        """全件検索（最大 5 件）"""
        try:
            items = list(self.container.read_all_items(max_item_count=5))

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
                "Failed to create user. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure

    def query_items(self, id) -> List[TimerManager]:
        """ID指定で検索"""
        try:
            logger.info("Querying for an  Item by Id {0}".format(id))

            items = list(
                self.container.query_items(
                    query="SELECT * FROM c WHERE c.id=@id",
                    parameters=[{"name": "@id", "value": id}],
                    enable_cross_partition_query=True,
                )
            )
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
                "Failed to create user. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure
