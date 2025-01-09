import json
import uuid
from datetime import datetime
from http import HTTPStatus

from core.entities.user import User
from infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository
from application.use_cases.create_user import CreateUserUseCase


def lambda_handler(event, context):
    timezone = datetime.now().astimezone().tzinfo

    try:
        # Parse request body
        body = json.loads(event['body'])

        # Validate required fields
        required_fields = ['username', 'email']
        missing_fields = [field for field in required_fields if field not in body]

        if missing_fields:
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'body': json.dumps({'error': 'Missing required fields', 'fields': missing_fields})
            }

        # Extract user data from request body
        username = body['username']
        email = body['email']

        # Generate a unique user ID and initialize a user entity
        user_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc)

        user = User(id=user_id, username=username, email=email, created_at=created_at)

        # Initialize repository and use case
        repository = DynamoDBUserRepository(table_name='Users')
        use_case = CreateUserUseCase(user_repository=repository)

        # Execute use case
        created_user = use_case.execute(user)

        return {
            'statusCode': HTTPStatus.CREATED,
            'body': json.dumps({'message': 'User created successfully', 'user': created_user.to_dict()})
        }

    except json.JSONDecodeError:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }

    except ValueError as e:
        # Handle specific business logic errors
        return {
            'statusCode': HTTPStatus.CONFLICT,
            'body': json.dumps({'error': str(e)})
        }

    except Exception as e:
        # Catch unexpected errors
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': 'An unexpected error occurred', 'details': str(e)})
        }
