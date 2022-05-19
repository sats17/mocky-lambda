import boto3
import os


def get_dynamodb_connection():
    """
    Creates boto3 DynamoDB connection.
    :return: DynamoDB Connection
    """
    print("Inside configuration_builder.get_dynamodb_connection() method")
    return boto3.client('dynamodb', region_name=os.environ['AWS_REGION'])  # hardcoded env for local test


print("Creating dynamodb connection from request service")
dynamodb_connection = get_dynamodb_connection()
print("Dynamodb connection = ", dynamodb_connection)

anime_table_name = os.environ['anime_table_name']
