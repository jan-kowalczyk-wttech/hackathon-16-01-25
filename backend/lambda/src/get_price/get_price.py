import json
import boto3

prompt = """

Human:

Please analyze this message, extract and provide information in JSON format with the following fields:
- price: (decimmal format eg. 10.99)
- currency: (USD, EUR, PLN etc.)
Please ensure the response is in valid JSON format.

Assistant:"""

region = "us-west-2"
runtime = boto3.client("bedrock-runtime", region)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    message = body["message"]

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": prompt,
            "messages": [
                {
                    "role": "user",
                    "content": message
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


    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }

