from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Initialize the Cosmos client
endpoint = "xxx"
key = "xxx"

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = "sample"
database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = "task_manager"
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/pk"),
    offer_throughput=400,
)
# </create_container_if_not_exists>


def select(id):

    # Query these items using the SQL query syntax.
    # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
    # <query_items>
    query = "SELECT * FROM c WHERE c.id = {0}".format(id)

    items = list(
        container.query_items(query=query, enable_cross_partition_query=True)
    )

    request_charge = container.client_connection.last_response_headers[
        "x-ms-request-charge"
    ]

    print(
        "Query returned {0} items. Operation consumed {1} request units".format(
            len(items), request_charge
        )
    )

    return items
