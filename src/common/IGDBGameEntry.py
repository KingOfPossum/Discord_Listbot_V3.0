from dataclasses import dataclass

@dataclass
class IGDBGameEntry:
    """
    A class containing the relevant information about a game retrieved from IGDB.
    """
    game_id: int
    game_name: str
    cover_url: str
    summary: str
    genres: list[str]
    platforms: list[str]