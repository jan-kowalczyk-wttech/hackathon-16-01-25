import json
import os

import boto3

s3_client = boto3.client('s3', "us-west-2")

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    object_name = "text.jpg"
    expiration = 3600

    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name, 'Key': object_name,'ContentType': 'image/jpeg'},
                                                    ExpiresIn=expiration)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'presigned_url': response})
    }