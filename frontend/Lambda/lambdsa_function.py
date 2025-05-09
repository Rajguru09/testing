## Make sure you are attached the file "bcrypt" Check in the steps >> bcrypt Zip file

import json
import boto3
import bcrypt  # Make sure this is packaged with your Lambda

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')  # Plain password from user input

    try:
        response = table.get_item(Key={'email': email})
        user = response.get('Item')

        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }

        # Compare using bcrypt
        hashed_password = user['password'].encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid password'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Login successful'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

