import boto3
import os
import json

region = "us-west-2"
runtime = boto3.client("bedrock-runtime", region)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['OFFER_CREATORS_TABLE'])

prompt = """

Human:
Please review the attached database row to ensure all fields are complete.
Response only in JSON format with the following fields:
- all_data_collected: (true if needed information is complete, false if not)
- answer: (a concise message for the user)
Identify any null or missing fields, and prioritize them by importance if multiple fields are incomplete. 

Based on your analysis, generate a very short, one sentence, concise, precise and friendly message for the user. 
The message should indicate which part of the book user should photograph to provide the missing information.
If all fields are complete, please indicate that all data has been collected.
Please ensure the response is in valid JSON format.

Assistant:"""
# prompt = """
#
# Human:
# Please analyze this image and provide information in JSON format with the following fields:
# - is_book: (true/false)
# Please ensure the response is in valid JSON format.
# Feel free to include any relevant details or observations in the answer field.
#
# Assistant:"""
def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = body.get("user_id")
    creator_id = body.get("creator_id")
    
    try:
        response = table.get_item(Key={'id': creator_id})
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
    
    