import json
from http import HTTPStatus

from simu_app.infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository

# from simu_app.infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository

def lambda_handler(event, context):
    try:
        # Get user ID from path parameters
        user_id = event['pathParameters'].get('id')
        if not user_id:
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'body': json.dumps({'error': 'User ID is required'})
            }

        # Initialize repository
        repository = DynamoDBUserRepository(table_name='Users')
        
        # Get user from DynamoDB
        user = repository.get_by_id(user_id)
        
        if not user:
            return {
                'statusCode': HTTPStatus.NOT_FOUND,
                'body': json.dumps({'error': 'User not found'})
            }

        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps(user.to_dict())
        }

    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': str(e)})
        }