from core.ports.user_repository import UserRepository


class GetAllUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self):
        """
        Executes a query to retrieve all users.
        Returns:
            list: A list of all users retrieved from the user repository.
        Args:
            None
        """
        return self.user_repository.get_all_users()
