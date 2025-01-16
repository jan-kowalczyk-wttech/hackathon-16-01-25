import json
import os
import traceback

import boto3

s3_client = boto3.client('s3', "us-west-2")

def lambda_handler(event, context):
    try:
        creator_id = event['pathParameters']['creator_id']
        user_id = event['pathParameters']['user_id']
        bucket_name = os.environ['BUCKET_NAME']
        expiration = 3600

        directory = f'{user_id}/{creator_id}/image'
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory)
        number_of_objects_in_directory = len(response.get('Contents', [1]))
        image_name = f"{number_of_objects_in_directory}.jpg"

        presigned_url = s3_client.generate_presigned_url('put_object',
                                                         Params={'Bucket': bucket_name, 'Key': f'{directory}/{image_name}', 'ContentType': 'image/jpeg'},
                                                         ExpiresIn=expiration)
        return {
            'statusCode': 200,
            'body': json.dumps({'presigned_url': presigned_url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'traceback': traceback.format_exc()
        }