import dataclasses

@dataclasses.dataclass
class UserEntry:
    user_id: int
    user_name: str
    display_name: str

    def __str__(self) -> str:
        return f"UserEntry:\n" +\
                f"  ID: {self.user_id}\n" +\
                f"  User Name: {self.user_name}\n" +\
                f"  Display Name: {self.display_name}\n"