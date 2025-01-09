import json
from infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository
from application.use_cases.get_all_users import GetAllUsersUseCase
from http import HTTPStatus


def lambda_handler(event, context):

    try:

        repository = DynamoDBUserRepository(table_name='Users')

        use_case = GetAllUsersUseCase(user_repository=repository)

        users = use_case.execute()



        return {
            'statusCode': HTTPStatus.OK,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(users)
        }

    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': str(e)})
        }
