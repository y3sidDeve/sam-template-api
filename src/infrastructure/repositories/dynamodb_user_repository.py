# Repository implementation for User entity using DynamoDB as storage
import boto3
import logging
from typing import Optional
from core.entities.user import User
from core.ports.user_repository import UserRepository
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        logger.debug(f"Creating user with data: {user_dict}")
        try:
            self.table.put_item(Item=user_dict)
            logger.info(f"User created successfully: {user_dict}")
        except ClientError as e:
            logger.error(f"Failed to create user: {
                         e.response['Error']['Message']}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID from DynamoDB
        Args:
            user_id: ID of the user to retrieve
        Returns:
            User entity if found, None otherwise
        """
        logger.debug(f"Retrieving user by ID: {user_id}")
        try:
            response = self.table.get_item(Key={'userId': user_id})
            item = response.get('Item')
            if item:
                logger.info(f"User retrieved successfully: {item}")
                return User.from_dict(item)
            else:
                logger.info(f"No user found with ID: {user_id}")
                return None

        except ClientError as e:
            logger.error(f"Failed to retrieve user: {
                         e.response['Error']['Message']}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email from DynamoDB using email-index
        Args:
            email: Email of the user to retrieve
        Returns:
            User entity if found, None otherwise
        """
        logger.debug(f"Retrieving user by email: {email}")
        try:
            response = self.table.query(
                IndexName='email-index',
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            items = response.get('Items', [])
            if items:
                logger.info(f"User retrieved successfully: {items[0]}")
                return User.from_dict(items[0])
            else:
                logger.info(f"No user found with email: {email}")
                return None
        except ClientError as e:
            logger.error(f"Failed to retrieve user: {
                         e.response['Error']['Message']}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    def get_all_users(self) -> list[User]:
        """
        Get all users from DynamoDB
        Returns:
            List of User entities
        """
        logger.debug("Retrieving all users")
        
        
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            
            users = items
            logger.info(f"Retrieved {len(users)} users")
            return users
        
        
        except ClientError as e:
            logger.error(f"Failed to retrieve users: {
                         e.response['Error']['Message']}"
                         )
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return []
