import boto3
import os
import json

region = "us-west-2"
runtime = boto3.client("bedrock-runtime", region)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['OFFER_CREATORS_TABLE'])

prompt = """
Please review the attached database row to ensure all fields are complete. 
Identify any null or missing fields, and prioritize them by importance if multiple fields are incomplete. 

Based on your analysis, generate a very short, one sentence, concise and friendly message for the user. 
The message should indicate which part of the book they should photograph to provide the missing information.
"""

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
    
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": prompt,
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(item)
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
        'statusCode': 200,
        'body': json.dumps({'message': response_body['content'][0]['text']})
    }
    
    