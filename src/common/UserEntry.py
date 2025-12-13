import dataclasses

@dataclasses.dataclass
class UserEntry:
    user_id: int
    user_name: str
    display_name: str

    def __str__(self):
        return f"User: ID: {self.user_id}, User Name: {self.user_name}, Display Name: {self.display_name}"