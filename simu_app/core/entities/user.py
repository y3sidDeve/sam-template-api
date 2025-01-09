from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: str
    username: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """
        Convert the User object to a dictionary.
        """
        return {
            'userId': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data: dict) -> 'User':
        """
        Create a User object from a dictionary.
        """
        return User(
            id=data['userId'], 
            username=data['username'],
            email=data['email'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )

