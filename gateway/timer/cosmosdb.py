import os

from azure.cosmos import CosmosClient

from .repository.timer_manager import TimerManagerRepository


class DatabaseConnection:
    def __init__(self, url, credential):
        # Initialize the Cosmos client
        self.client = CosmosClient(
            url=url,
            credential=credential,
        )

        # Read a database
        self.database = self.client.get_database_client(
            os.environ["COSMOS_DATABASE"]
        )

    def timer_manager(self):
        return TimerManagerRepository(self.database)
