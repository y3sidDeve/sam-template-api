import json
from http import HTTPStatus
from application.use_cases.get_user_by_id import GetUserByIdUseCase
from infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository


def lambda_handler(event, context):
    try:
        # Obtener el user_id de los parámetros del evento
        user_id = event['pathParameters'].get('user_id')

        # Inicializar el repositorio y el caso de uso
        repository = DynamoDBUserRepository(table_name='Users')
        use_case = GetUserByIdUseCase(user_repository=repository)

        # Ejecutar el caso de uso
        user = use_case.execute(user_id)

        if not user:
            return {
                'statusCode': HTTPStatus.NOT_FOUND,
                "headers": {"Content-Type": "application/json"},
                'body': json.dumps({'error': 'User not found'})
            }

        # Responder con los datos del usuario
        return {
            'statusCode': HTTPStatus.OK,
            "headers": {"Content-Type": "application/json"},
            'body': json.dumps(user.to_dict())
        }

    except ValueError as e:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            "headers": {
                "Content-Type": "application/json"
            },
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            "headers": {"Content-Type": "application/json"},
            'body': json.dumps({'error': str(e)})
        }
