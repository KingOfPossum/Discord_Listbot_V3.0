import discord

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.GameEntry import GameEntry
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.Database import Database
from discord.ext import commands

class ViewCommand(Command):

    def __init__(self,database: Database):
        self.database = database

    @staticmethod
    def get_game_view_txt(game_entry: GameEntry) -> str:
        """
        Creates an embed for the game view command.
        Contains all information about the game entry.
        :param game_entry: The GameEntry containing the game details.
        :return : A formatted string with the game details.
        """
        console_emoji = Emojis.CONSOLES[game_entry.console] if Emojis.CONSOLES[
                                                                   game_entry.console] != "" else game_entry.console

        view_game_details = f"**Console:** {console_emoji}\n" \
                            f"**Rating:** {game_entry.rating}\n" \
                            f"**Genre:** {game_entry.genre}\n" \
                            f"**Review:** {game_entry.review}\n\n" \
                            f"**Replay:** {[Emojis.CROSS_MARK, Emojis.CHECK_MARK][game_entry.replayed]}\n\n" \
                            f"Added on **{game_entry.date}**"

        return view_game_details


    @commands.command(name="view")
    async def execute(self, ctx):
        """
        Handles the 'view' command to view the game details of a specific game.
        This command will check if the game exists in the database and then display its details.
        If the game does not exist, it will send an error message.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        game_name=  BotUtils.get_message_content(ctx.message)
        game = await BotUtils.game_exists(game_name,self.database,ctx=ctx)
        if not game:
            return

        game_name, game_entry = game

        embed = MessageManager.get_embed(title=f"**{game_name} {"(100%)" * game_entry.hundred_percent}**",description=self.get_game_view_txt(game_entry))
        await MessageManager.send_message(ctx.channel,embed=embed)

    def help(self) -> str:
        return f"- `{ConfigLoader.get_config().command_prefix}view` `gameName` - View the details of a game in the list\n"