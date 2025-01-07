# Repository implementation for User entity using DynamoDB as storage
import boto3
from typing import Optional
from simu_app.domain.entities.user import User 
from simu_app.domain.ports.user_repository import UserRepository

class DynamoDBUserRepository(UserRepository):
    """
    Repository class that implements UserRepository interface using DynamoDB
    """
    
    def __init__(self, table_name: str):
        """
        Initialize repository with DynamoDB table name
        Args:
            table_name: Name of the DynamoDB table to use
        """
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def create(self, user: User) -> User:
        """
        Create a new user in DynamoDB
        Args:
            user: User entity to create
        Returns:
            Created User entity
        """
        user_dict = user.to_dict()
        self.table.put_item(Item=user_dict)
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID from DynamoDB
        Args:
            user_id: ID of the user to retrieve
        Returns:
            User entity if found, None otherwise
        """
        response = self.table.get_item(Key={'id': user_id})
        item = response.get('Item')
        return User.from_dict(item) if item else None

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email from DynamoDB using email-index
        Args:
            email: Email of the user to retrieve
        Returns:
            User entity if found, None otherwise
        """
        response = self.table.query(
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        items = response.get('Items', [])
        return User.from_dict(items[0]) if items else None
