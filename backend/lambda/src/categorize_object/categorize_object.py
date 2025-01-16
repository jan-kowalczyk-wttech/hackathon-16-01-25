
import base64
import json
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


def lambda_handler(event, context):
    uuid = event.get("uuid")

    image = s3_client.get_object(
        Bucket=os.environ['BUCKET_NAME'],
        Key=f"{uuid}/image.jpg"
    )

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

    return {
        "statusCode": 200,
        "body": json.dumps(response_body['content'][0]['text'])
    }
