import dataclasses

@dataclasses.dataclass(frozen=False)
class BacklogEntry:
    """
    Entry in the backlog.
    Attributes:
        name: The name of the game.
        user: The user who has this game in their backlog.
        recommended_by: The user who recommended this game, if any.
    """
    name: str
    user: str
    recommended_by: str = None