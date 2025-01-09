from core.ports.user_repository import UserRepository
from core.entities.user import User


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository): ## RECIBE EL REPOSITORIO
        self.user_repository = user_repository

    def execute(self, user: User) -> User:
        """
        Execute the user creation use case.
        Args:
            user: User entity to create.
        Returns:
            The created user.
        Raises:
            ValueError: If a user with the same email already exists.
        """
        # Check if user already exists by email
        existing_user = self.user_repository.get_by_email(user.email)
        if existing_user:
            raise ValueError(f"A user with the email {
                             user.email} already exists."
                            )

        # Create the user
        return self.user_repository.create(user)
