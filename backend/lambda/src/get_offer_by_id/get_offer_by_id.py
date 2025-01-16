import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['OFFERS_TABLE'])


def lambda_handler(event, context):
    offer_id = event['pathParameters']['id']

    try:
        response = table.get_item(Key={'id': offer_id})
        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Offer not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'offer': item})
    }