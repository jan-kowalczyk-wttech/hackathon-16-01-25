
import base64
import json
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
- answer: (maintain conversation with user and ask about missing fields)
Please ensure the response is in valid JSON format.
If any information cannot be determined from the image, use null for that field.
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
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": prompt},
                    ],
                },
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
