from abc import ABC, abstractmethod
from typing import Optional
from core.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user in the repository"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email"""
        pass
    
    @abstractmethod
    def get_all_users(self) -> list[User]:
        """Retrieve all users"""
        pass