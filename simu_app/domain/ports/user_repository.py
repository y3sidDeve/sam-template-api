from abc import ABC, abstractmethod
from typing import Optional
from simu_app.domain.entities.user import User

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