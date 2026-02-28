import dataclasses

@dataclasses.dataclass(frozen=False)
class BacklogEntry:
    """
    Entry in the backlog.
    Attributes:
        game_name: The name of the game.
        user_id: The ID of the user who has this game in their backlog.
        recommended_by_user: The ID of the user who recommended this game, if any.
    """
    game_name: str
    user_id: int
    recommended_by_user: id = None

    def __str__(self) -> str:
        return "BacklogEntry:\n" \
                f"  Game Name: {self.game_name}\n" \
                f"  User ID: {self.user_id}\n" \
                f"  Recommended By User ID: {self.recommended_by_user}\n"