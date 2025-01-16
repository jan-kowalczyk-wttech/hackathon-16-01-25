
import base64
import json
import traceback
import uuid
from typing import Any

import boto3
import os

prompt = """

Human:
Please analyze this image and provide information in JSON format with the following fields:
- title: (book's title, or null if not visible)
- author: (author's name, or null if not visible)
- isbn: (ISBN number if visible, or null if not present)
- language: (book's language, or null if not certain)
- publisher: (publisher's name and year of publication, or null if not visible)
- cover_type: (hardcover/softcover/other, or null if not visible)
- condition: (book's physical condition if assessable from image, or null if not clear)
- description: (create an engaging marketing description highlighting the book's key features, condition, and appeal to potential readers. Focus on unique selling points, special features, and why someone should be interested in this book. Use persuasive and professional language.)
Please ensure the response is in valid JSON format.
If any information cannot be determined from the image, use null for that field.

Assistant:"""

region = "us-west-2"
runtime = boto3.client("bedrock-runtime", region)
s3_client = boto3.client("s3", region)
dynamodb = boto3.resource("dynamodb", region)


def get_combines_results(creator_results, result):
    all_items = {}
    for creator_result in creator_results:
        data = creator_result["result"]
        if not isinstance(data, dict):
            data = json.loads(creator_result["result"])
        print(data)
        for key, value in data.items():
            if all_items.get(key) is None or value is not None:
                all_items.update({key: value})

    if not isinstance(result, dict):
        result = json.loads(result)

    for key, value in result.items():
        if all_items.get(key) is None or value is not None:
            all_items.update({key: value})

    return all_items

def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = body.get("user_id")
    creator_id = body.get("creator_id")
    bucket_name = os.environ['BUCKET_NAME']
    action_table = os.environ['ACTIONS_TABLE']

    directory = f'{user_id}/{creator_id}/image'
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory)

    image = response['Contents'][-1]
    image = s3_client.get_object(Bucket=bucket_name, Key=image['Key'])

    image_bytes = image['Body'].read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": encoded_image,
                            },
                        }
                    ]
                }
            ],
        }
    )

    response = runtime.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=body
    )
    response_body = json.loads(response.get("body").read())
    result = response_body['content'][0]['text']

    responses = dynamodb.Table(action_table).scan().get('Items')
    creator_results = []
    for response in responses:
        if response['creator_id'] == creator_id and response["action_name"] == "define_object":
            creator_results.append(response)

    result = get_combines_results(creator_results, result)

    item = get_action_item(user_id, creator_id, result)
    dynamodb.Table(action_table).put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }

def get_action_item(user_id: str, creator_id: str, result: Any):
    id = str(uuid.uuid4())
    action_name = "define_object"
    return {
        "id": id,
        "user_id": user_id,
        "creator_id": creator_id,
        "action_name": action_name,
        "result": result
    }