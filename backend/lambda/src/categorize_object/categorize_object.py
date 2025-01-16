
import base64
import json
import uuid

import boto3
import os

prompt = """

Human:
Please analyze this image and provide information in JSON format with the following fields:
- is_book: (true/false)
- answer: (maintain conversation with user)
Please ensure the response is in valid JSON format.
Feel free to include any relevant details or observations in the answer field.

Assistant:"""

region = "us-west-2"
runtime = boto3.client("bedrock-runtime", region)
s3_client = boto3.client("s3", region)
dynamodb = boto3.resource("dynamodb", region)
action_name = "categorize_object"


def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = body['user_id']
    creator_id = body['creator_id']
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

    dynamodb.Table(action_table).put_item(Item={"id": str(uuid.uuid4()), "user_id": user_id, "action_name": action_name, result: result})

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
