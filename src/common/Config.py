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
    bot_replies: bool
    bot_replies_to_links: bool
    bot_replies_users: set[str]
    accepted_users: set[str]
    consoles: dict[str, str]

    def __str__(self):
        return  "-" *100 + "\n" \
                f"Config:\n" \
                f"  Command Prefix: {self.command_prefix}\n" \
                f"  Database Folder Path: {self.database_folder_path}\n" \
                f"  Bot Replies: {self.bot_replies}\n" \
                f"  Bot Replies to Links: {self.bot_replies_to_links}\n" \
                f"  Bot Replies Users: {self.bot_replies_users}\n" \
                f"  Accepted Users: {self.accepted_users}\n" \
                f"  Consoles: {self.consoles}\n" \
                + "-" * 100 + "\n"