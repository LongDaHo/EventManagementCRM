import boto3

dynamodb = boto3.client("dynamodb", region_name="ap-southeast-1")
table_name = "crm-users-table"

# Optional: clean up if exists
try:
    dynamodb.delete_table(TableName=table_name)
    waiter = dynamodb.get_waiter("table_not_exists")
    waiter.wait(TableName=table_name)
except dynamodb.exceptions.ResourceNotFoundException:
    pass

# Create the table with 5 GSIs
response = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"},
    ],
    AttributeDefinitions=[
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
        {"AttributeName": "company", "AttributeType": "S"},
        {"AttributeName": "jobTitle", "AttributeType": "S"},
        {"AttributeName": "city", "AttributeType": "S"},
        {"AttributeName": "state", "AttributeType": "S"},
        {"AttributeName": "hostedEvents", "AttributeType": "N"},
        {"AttributeName": "attendedEvents", "AttributeType": "N"},
    ],
    GlobalSecondaryIndexes=[
        {
            "IndexName": "GSI_Company",
            "KeySchema": [
                {"AttributeName": "company", "KeyType": "HASH"},
                {"AttributeName": "PK", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "KEYS_ONLY"},
        },
        {
            "IndexName": "GSI_JobTitle",
            "KeySchema": [
                {"AttributeName": "jobTitle", "KeyType": "HASH"},
                {"AttributeName": "PK", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "KEYS_ONLY"},
        },
        {
            "IndexName": "GSI_CityState",
            "KeySchema": [
                {"AttributeName": "state", "KeyType": "HASH"},
                {"AttributeName": "city", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "KEYS_ONLY"},
        },
        {
            "IndexName": "GSI_HostedEvents",
            "KeySchema": [
                {"AttributeName": "hostedEvents", "KeyType": "HASH"},
                {"AttributeName": "PK", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "KEYS_ONLY"},
        },
        {
            "IndexName": "GSI_AttendedEvents",
            "KeySchema": [
                {"AttributeName": "attendedEvents", "KeyType": "HASH"},
                {"AttributeName": "PK", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "KEYS_ONLY"},
        },
    ],
    BillingMode="PAY_PER_REQUEST",
)

print("DynamoDB table with 5 GSIs is being created...")
