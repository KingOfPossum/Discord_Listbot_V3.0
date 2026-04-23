import requests
import re

class MetacriticSearcher:
    """
    Class for searching metacritic.
    """
    @staticmethod
    def get_metacritic_score(game_title:str) -> int | None:
        """
        Searches metacritic for the given game and returns the metascore.
        If game not found returns None.
        :param game_title: The title of the game.
        :return: The metascore or None
        """
        # Needed to access metacritic
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }

        # Get the metacritic page for the game
        response = requests.get("https://www.metacritic.com/game/" + MetacriticSearcher.format_game_title(game_title),headers=headers)

        # Check if search for the page was successful
        if response.status_code != 200:
            print("Error: " + str(response.status_code))
            return None

        # Get the metacritic score from the page
        regex = re.compile(r'"ratingValue":\d+')
        val = regex.search(response.text)
        if not val:
            return None
        val = val.group()
        regex = re.compile(r'\d+')
        return int(regex.search(val).group())

    @staticmethod
    def format_game_title(game_title:str) -> str:
        """
        Formats the game_title for better accuracy when searching metacritic.
        :param game_title: The title of the game.
        :return: The formatted game title.
        """
        game_title = "-".join(game_title.lower().split())
        game_title = game_title.replace(":", "")
        game_title = game_title.replace("&", "and")
        game_title = game_title.replace("(", "")
        game_title = game_title.replace(")", "")

        return game_title