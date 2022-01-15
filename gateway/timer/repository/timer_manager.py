from logging import getLogger

from azure.cosmos import DatabaseProxy, exceptions

logger = getLogger(__name__)


class TimerManagerRepository:
    def __init__(self, database: DatabaseProxy) -> None:
        self.container = database.get_container_client("task_manager")

    def read_all_items(self):
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
            return items

        except exceptions.CosmosHttpResponseError as failure:
            logger.error(
                "Failed to create user. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure

    def query_items(self, id):
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
            return items

        except exceptions.CosmosHttpResponseError as failure:
            logger.error(
                "Failed to create user. Status code:{}".format(
                    failure.status_code
                )
            )
            raise failure
