import json
import base64
import boto3
import os

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    try:
        bucket_name = os.environ['BUCKET_NAME']
        creator_id = event['pathParameters']['creator_id']
        user_id = event['pathParameters']['user_id']

        directory = f'{user_id}/{creator_id}/image'
        response = s3_client.get_object(Bucket=bucket_name, Key=f"{directory}/1.jpg")
        image_bytes = response['Body'].read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': encoded_image
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }