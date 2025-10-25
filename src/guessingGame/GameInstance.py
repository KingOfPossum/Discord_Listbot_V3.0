import random

from common.GameEntry import GameEntry
from common.MessageManager import MessageManager
from database.ListDatabase import ListDatabase
from discord.ext import commands
from guessingGame.GuessGameEntry import GuessGameEntry

class GameInstance:
    GUESSES_FOR_LOSS = 5

    def __init__(self, database: ListDatabase,ctx: commands.Context):
        self.database: ListDatabase = database
        self.ctx: commands.Context = ctx
        self.game:GuessGameEntry = self.get_random_game()
        self.guesses = 0
        self.game_over = False

        print(self.game)

    def get_random_game(self) -> GuessGameEntry:
        """
        Returns a random game from the database
        :return: The GuessGameEntry instance containing all information about the game that was chosen
        """
        game_entries:list[GameEntry] = self.database.get_all_game_entries()
        game_entry:GameEntry = random.choice(game_entries)

        return GuessGameEntry.load(game_entry.name,game_entry.console,self.database)

    def make_guess(self,name:str):
        """
        Checks if a guess is correct. If it is the game is over and the players win.
        Otherwise, give another hint. If the amount of guesses made till this point are greater than
        GUESSES_FOR_LOSS, the game is also over as the players loose.
        :param name: The name of the game which was guessed
        :return: True if the guess was correct, False otherwise
        """
        if self.game.name == name:
            MessageManager.send_message(self.ctx.channel,f"Congratulations! The game was {self.game.name}!!!")
            self.game_over = True
        else:
            self.guesses += 1
            if self.guesses >= self.GUESSES_FOR_LOSS:
                MessageManager.send_message(self.ctx.channel,f"Wrong! The game is over! The game was {self.game.name}!!!")
                self.game_over = True
                return
            self.give_hint()

    def give_hint(self):
        """
        Gives a hint about the game
        """
        if self.guesses == 0:
            MessageManager.send_message(self.ctx.channel,"")