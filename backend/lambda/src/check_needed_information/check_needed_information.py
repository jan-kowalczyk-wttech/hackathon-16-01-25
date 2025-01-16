import traceback

import boto3
import os
import json

region = "us-west-2"
runtime = boto3.client("bedrock-runtime", region)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ACTIONS_TABLE'])

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

def get_empty_items(creator_results):
    try:
        all_items = {}
        for creator_result in creator_results:
            data = json.loads(creator_result["result"])
            print(data)
            for key, value in data.items():
                if all_items.get(key) is None:
                    all_items.update({key: value})

        null_items = {}
        for key, value in all_items.items():
            if value is None:
                null_items.update({key: value})

        return null_items
    except Exception as e:
        print(e)
        traceback.print_exc()

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        creator_id = body['creator_id']

        responses = table.scan().get('Items')
        creator_results = []
        for response in responses:
            if response['creator_id'] == creator_id and response["action_name"] == "define_object":
                creator_results.append(response)

        empty_items = get_empty_items(creator_results)

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": json.dumps(empty_items)
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