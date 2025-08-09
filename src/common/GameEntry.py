from dataclasses import dataclass

@dataclass(frozen=False)
class GameEntry:
    """
    Represents a game entry in the database.
    This class is used to store information about a game, including its name, user, date, console, rating, genre, and review.
    """
    name: str
    user: str
    date: str
    console: str
    rating: int
    genre: str
    review: str
    replayed: bool = False
    hundred_percent: bool = False

    def __str__(self) -> str:
        return f"GameEntry:\n" \
               f"  Name: {self.name}\n" \
               f"  User: {self.user}\n" \
               f"  Date: {self.date}\n" \
               f"  Console: {self.console}\n" \
               f"  Rating: {self.rating}\n" \
               f"  Genre: {self.genre}\n" \
               f"  Review: {self.review}\n" \
               f"  Replayed: {self.replayed}\n" \
               f"  Hundred Percent: {self.hundred_percent}"