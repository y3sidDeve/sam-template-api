import json
from http import HTTPStatus
from infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository


def lambda_handler(event, context):
    try:
        # Get user ID from path parameters
        user_id = event['pathParameters'].get('user_id')

        
        print(f'user ID es: {user_id}')
        
        if not user_id:
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                "headers": {
                    "Content-Type": "application/json"
                },
                'body': json.dumps({'error': 'User ID is required'})
            }

        # Initialize repository
        repository = DynamoDBUserRepository(table_name='Users')

        # Get user from DynamoDB
        user = repository.get_by_id(user_id)
        
        
        print(f"User: {user}")

        if not user or user is None:
            
            print('not user')
            return {
                'statusCode': HTTPStatus.NOT_FOUND,
                "headers": {
                    "Content-Type": "application/json"
                },
                'body': json.dumps({'error': 'User not found'})
            }

        # Return user data in response
        return {
            'statusCode': HTTPStatus.OK,
            "headers": {
                "Content-Type": "application/json"
            },
            # Assumes the User class has a to_dict() method
            'body': json.dumps(user.to_dict())
        }

    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({'error': str(e)})
        }
