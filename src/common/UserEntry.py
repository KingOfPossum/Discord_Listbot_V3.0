import dataclasses

@dataclasses.dataclass
class UserEntry:
    user_id: int
    user_name: str
    display_name: str

    def __str__(self) -> str:
        return f"""
                UserEntry:\n
                    ID: {self.user_id}\n
                    User Name: {self.user_name}\n
                    Display Name: {self.display_name}
                """