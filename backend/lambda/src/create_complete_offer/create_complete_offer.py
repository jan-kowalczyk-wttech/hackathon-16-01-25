import json
import os
import uuid
from datetime import datetime
import traceback
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def get_combines_results(creator_results):
    all_items = {}
    for creator_result in creator_results:
        data = creator_result["result"]
        if not isinstance(data, dict):
            data = json.loads(creator_result["result"])
        print(data)
        for key, value in data.items():
            if all_items.get(key) is None or value is not None:
                all_items.update({key: value})

    return all_items

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        creator_id = body['creator_id']
        action_table = os.environ['ACTIONS_TABLE']
        offer_table = os.environ['OFFER_CREATORS_TABLE']

        responses = dynamodb.Table(action_table).scan().get('Items')
        creator_results = []
        for response in responses:
            if response['creator_id'] == creator_id and response["action_name"] == "define_object":
                creator_results.append(response)

        result = get_combines_results(creator_results)

        item = get_offer_item(user_id, creator_id, result, body)
        dynamodb.Table(offer_table).put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        print(e)
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_offer_item(user_id: str, creator_id: str, result: Any, body):
    id = str(uuid.uuid4())
    return {
        "id": id,
        "user_id": user_id,
        "creator_id": creator_id,
        "title": result.get("title"),
        'author': result.get('author'),
        'isbn': result.get('isbn'),
        'language': result.get('language'),
        'publisher': result.get('publisher'),
        'cover_type': result.get('cover_type'),
        'price': body.get('price'),
        'condition': body.get('condition'),
    }
