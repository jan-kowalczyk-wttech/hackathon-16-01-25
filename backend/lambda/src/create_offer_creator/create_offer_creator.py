import json
import os
import traceback

import boto3
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['OFFER_CREATORS_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        id = str(uuid4())

        existing_items = table.scan().get('Items')
        for item in existing_items:
            if item['user_id'] == user_id and item['is_active'] == True:
                print(f'Offer creator {user_id} already exists')
                print(f'Shutting down old offer creator {item["id"]}')
                table.update_item(
                    Key={
                        'id': item['id']
                    },
                    UpdateExpression='SET is_active = :val',
                    ExpressionAttributeValues={
                        ':val': False
                    }
                )
        item = {
            'id': id,
            'user_id': user_id,
            'is_active': True
        }
        table.put_item(Item=item)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': f'Offer creator {id} created successfully'}),
        }
    except Exception as e:
        print(e)
        traceback.print_exception(type(e), value=e, tb=e.__traceback__)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'traceback': traceback.format_exc()}),
        }