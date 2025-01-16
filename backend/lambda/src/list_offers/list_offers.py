
import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['OFFERS_TABLE'])

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items')
        if not items:
            print("Could not find any offers")
            items = []

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'offers': items})
    }