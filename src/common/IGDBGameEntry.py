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

    def __str__(self):
        return f"IGDBGameEntry:\n"\
               f"   Game ID: {self.game_id}\n" \
               f"   Game Name: {self.game_name}\n" \
               f"   Cover URL: {self.cover_url}\n" \
               f"   Summary: {self.summary}\n" \
               f"   Genres: {', '.join(self.genres)}\n" \
               f"   Platforms: {', '.join(self.platforms)}"