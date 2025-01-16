import json


def lambda_handler(event, context):
    body = json.loads(event.get('body'))
    message = body.get('message')
    is_image = body.get('is_image')

    return {
        'statusCode': 200,
        'body': json.dumps({'message': message, 'is_image': is_image})
    }
