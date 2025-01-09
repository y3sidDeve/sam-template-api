from core.entities.user import User
from core.ports.user_repository import UserRepository
from typing import Optional


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> Optional[User]:
        """
        Ejecuta la lógica para obtener un usuario por su ID.
        Args:
            user_id (str): ID del usuario.
        Returns:
            Optional[User]: El usuario encontrado, o None si no existe.
        """
        if not user_id:
            raise ValueError("User ID is required")
        return self.user_repository.get_by_id(user_id)
