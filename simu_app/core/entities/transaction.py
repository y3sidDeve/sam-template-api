from datetime import datetime
from uuid import uuid4


class Transaction:
    
    def __init__(self, amount: float, description: str, user_id: str):
        timezone = datetime.now().astimezone().tzinfo

        self.id = str(uuid4())  # Generar un ID único
        self.amount = amount
        self.description = description
        self.user_id = user_id
        self.created_at = datetime.now(timezone.utc)


    def is_valid(self) -> bool:
        # Lógica de negocio para validar una transacción
        return self.amount > 0

    def to_dict(self):
        # Convierte la entidad en un diccionario para persistirla o serializarla
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
        }
