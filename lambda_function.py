from configuration.configuration_builder import dynamodb_connection, anime_table_name


def lambda_handler(event, context):
    print("Incoming event ", event)
    anime_name = str(event['anime_name'])
    response = dynamodb_connection.query(
        TableName=anime_table_name,
        KeyConditionExpression='anime_name = :anime_name',
        ExpressionAttributeValues={
            ':anime_name': {'S': anime_name}
        }
    )

    anime_info = response['Items'][0]
    print(anime_info)
    return {"main_character": anime_info["main_character"]["S"]}
