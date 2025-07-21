import boto3

dynamodb = boto3.client("dynamodb", region_name="ap-southeast-1")
table_name = "crm-events-table"

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
    ],
    BillingMode="PAY_PER_REQUEST",
)

print("DynamoDB table being created...")
