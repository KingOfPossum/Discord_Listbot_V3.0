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
