import json
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['OFFER_CREATORS_TABLE'])

def lambda_handler(event, context):
    user_id = event['pathParameters']['user_id']

    try:
        response = table.scan().get('Items')
        active_item = None
        for item in response:
            if item['user_id'] == user_id and item['is_active'] == True:
                active_item = item

        if active_item is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No active offer creators found'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'offer_creator': active_item})
    }