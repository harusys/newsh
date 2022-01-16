from datetime import datetime, time, timedelta
from logging import getLogger
from typing import List

from azure.cosmos import DatabaseProxy, exceptions
from pydantic import BaseModel, parse_obj_as

logger = getLogger(__name__)


class TimerManager(BaseModel):
    user_id: str
    task_name: str
    scheduled_at: time
    is_enabled: bool


class TimerManagerRepository:
    """タイマ管理コンテナ用クラス"""

    def __init__(self, database: DatabaseProxy) -> None:
        self.container = database.get_container_client("task_manager")

    def find_by_time(self, current_time: datetime) -> List[TimerManager]:
        """時刻指定で検索（スケジュールは前後 5 分で検索）"""
        try:
            logger.info("Querying for Items by time {0}".format(current_time))

            items = list(
                self.container.query_items(
                    query="SELECT * FROM c"
                    + " WHERE @start_time <= c.scheduled_at"
                    + " AND c.scheduled_at <= @end_time"
                    + " AND c.is_enabled = @is_enabled",
                    parameters=[
                        # 時刻ズレを考慮して現在時刻 ± 5 分で抽出
                        {
                            "name": "@start_time",
                            "value": (
                                current_time + timedelta(minutes=-5)
                            ).strftime("%H:%M:%S"),
                        },
                        {
                            "name": "@end_time",
                            "value": (
                                current_time + timedelta(minutes=5)
                            ).strftime("%H:%M:%S"),
                        },
                        # 有効なレコードのみ
                        {"name": "@is_enabled", "value": "True"},
                    ],
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
