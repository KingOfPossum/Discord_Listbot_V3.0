import dataclasses

from common.Wrapper import Wrapper
from database.ListDatabase import ListDatabase
from Game import Game

@dataclasses.dataclass
class GuessGameEntry:
    name: str
    genres: list
    consoles: list
    reviews: list
    played_by: list
    screenshots: list
    release_date: str

    @classmethod
    def load(cls, name: str, console: str, database: ListDatabase):
        """
        Loads an GameEntry
        :param name: Name of the game
        :param console: Name of the console the game was played with in the database
        :param database: The ListDatabase instance
        :return: The GameEntry instance
        """
        game: Game = Game.from_igdb(Wrapper.wrapper, name, console)
        game.load_all()
        game_entries = database.get_all_instances_of_game(name)

        return GuessGameEntry(name=name, genres=game.genres, consoles=game.platforms,
                         reviews=[entry.review for entry in game_entries],
                         played_by=list(set([entry.user for entry in game_entries])),
                         screenshots=game.screenshots,
                         release_date=game.release_dates[0])

    def __str__(self) -> str:
        return f"Name: {self.name}\n" +\
                f"Genres: {self.genres}\n" +\
                f"Consoles: {self.consoles}\n" +\
                f"Reviews: {self.reviews}\n" +\
                f"Played By: {self.played_by}\n" +\
                f"Screenshots: {self.screenshots}\n" +\
                f"Release Date: {self.release_date}\n"