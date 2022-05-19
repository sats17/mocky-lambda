import unittest

import boto3
import os
from moto import mock_dynamodb
from unittest.mock import patch


@mock_dynamodb  # Decorator applied to whole class for providing mock for each dynamodb calls
@patch.dict(os.environ, {
    "AWS_REGION": "us-east-1",
    "anime_table_name": 'anime_info'})
class LambdaFunctionTest(unittest.TestCase):

    def setUp(self) -> None:
        print("Setup invoked for testing suite")
        self.dynamodb = boto3.resource('dynamodb', 'us-east-1')
        anime_table_name = 'anime_info'
        self.dynamodb.create_table(TableName=anime_table_name,
                                   KeySchema=anime_table_data['KeySchema'],
                                   AttributeDefinitions=anime_table_data['AttributeDefinitions'],
                                   ProvisionedThroughput=anime_table_data['ProvisionedThroughput']
                                   )

        self.registration_status_table = self.dynamodb.Table(anime_table_name)

    def test_get_pending_request_success(self):
        registration_status_data_list = [
            {"anime_name": "naruto", "main_character": "naruto"},
            {"anime_name": "attack on titan", "main_character": "eren"},
            {"anime_name": "demon slayer", "main_character": "tanjiro"}
        ]
        for data in registration_status_data_list:
            self.registration_status_table.put_item(Item=data)

        print("test case started")
        """
        Importing lambda_function here because we have some AWS resources are eager loading type(Defined outside of the
        function). If we import this file at top, those eager loaded AWS resources will start executing and they will 
        try to call real AWS components. So we are importing file after setting up mocks.
        """
        import lambda_function
        response = lambda_function.lambda_handler({"anime_name": "naruto"}, None)
        print(response)
        expected_response = {'main_character': 'naruto'}
        self.assertEqual(response, expected_response)

    # def test_get_zero_pending_request(self):
    #     user_data_list = [
    #         {'user_email': 'satish@test.com', 'user_status': 'APPROVED'},
    #         {'user_email': 'satiar@test.com', 'user_status': 'REJECTED'}
    #     ]
    #     for data in user_data_list:
    #         self.registration_status_table.put_item(Item=data)
    #     import lambda_function
    #     response = lambda_function.lambda_handler({"EventName": "ListAllPendingRequest"}, None)
    #     expected_response = {'status': 'success', 'statusCode': 200, 'body': []}
    #     self.assertEqual(response, expected_response)
    #
    # def test_invalid_event_in_request_body(self):
    #     import lambda_function
    #     response = lambda_function.lambda_handler({"EventName": "InvalidEvent"}, None)
    #     expected_response = {'status': 'Bad Request', 'statusCode': 400, 'body': 'Invalid Event'}
    #     self.assertEqual(response, expected_response)
    #
    # def test_invalid_event_schema_in_request_body(self):
    #     import lambda_function
    #     response = lambda_function.lambda_handler({"InvalidEventNameKey": "InvalidEvent"}, None)
    #     expected_response = {'status': 'bad request', 'statusCode': 400, 'body': 'EventName not present in incoming '
    #                                                                              'event'}
    #     print(response)
    #     self.assertEqual(response, expected_response)

    def tearDown(self) -> None:
        print("Tearing down resources")
        self.registration_status_table.delete()


anime_table_data = {
    'KeySchema': [{
        'AttributeName': 'anime_name',
        'KeyType': 'HASH'
        }
    ],
    'AttributeDefinitions': [
        {
            'AttributeName': 'anime_name',
            'AttributeType': 'S'
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
}

user_table_data = {
    'KeySchema': [{
        'AttributeName': 'user_id',
        'KeyType': 'HASH'
    },
        {
            'AttributeName': 'registration_id',
            'KeyType': 'RANGE'
        }
    ],
    'AttributeDefinitions': [
        {
            'AttributeName': 'user_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'registration_id',
            'AttributeType': 'S'
        }
    ],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
}
