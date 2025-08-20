from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    """
    Represents the configuration for the application.
    This class is used to store various settings such as database path, console list, and other configurations.
    """
    api_key: str
    command_prefix: str
    database_folder_path: str
    accepted_users: set[str]
    consoles: dict[str, str]

    def __str__(self):
        return  "-" *100 + "\n" \
                f"Config:\n" \
                f"  Command Prefix: {self.command_prefix}\n" \
                f"  Database Folder Path: {self.database_folder_path}\n" \
                f"  Accepted Users: {self.accepted_users}\n" \
                f"  Consoles: {self.consoles}\n" \
                + "-" * 100 + "\n"