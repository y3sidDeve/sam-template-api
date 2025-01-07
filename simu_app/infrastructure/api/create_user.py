import json
import uuid
from datetime import datetime
from http import HTTPStatus

from simu_app.domain.entities.user import User
from simu_app.infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        
        print(json.dumps(body))
        
        # Validate required fields
        required_fields = ['username', 'email']
        if not all(field in body for field in required_fields):
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        # Create user instance
        user = User(
            id=str(uuid.uuid4()),
            username=body['username'],
            email=body['email'],
            created_at=datetime.utcnow()
        )

        # Initialize repository
        repository = DynamoDBUserRepository(table_name='Users')
        
        # Check if user with email already exists
        existing_user = repository.get_by_email(user.email)
        if existing_user:
            return {
                'statusCode': HTTPStatus.CONFLICT,
                'body': json.dumps({'error': 'User with this email already exists'})
            }

        # Save user to DynamoDB
        created_user = repository.create(user)

        return {
            'statusCode': HTTPStatus.CREATED,
            'body': json.dumps(created_user.to_dict())
        }

    except json.JSONDecodeError:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': str(e)})
        }