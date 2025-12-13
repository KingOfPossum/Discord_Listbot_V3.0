from common.BacklogEntry import BacklogEntry
from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database_.BacklogDatabase import BacklogDatabase
from discord.ext import commands

class RecommendCommand(Command):
    """
    A command to recommend a game to another user.
    """
    def __init__(self,backlog_database:BacklogDatabase):
        self.backlog_database = backlog_database

    @commands.command(name="recommend",aliases=["recommendGame","recommend_game","Recommend","RecommendGame","Recommend_Game","RECOMMEND_GAME"])
    async def execute(self, ctx):
        """
        Recommends a game to another user.
        Checks if the user is valid and adds the recommendation as a new BacklogEntry object to the backlog database.
        :param ctx: The context of the command.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        message_content = BotUtils.get_message_content(ctx.message)
        args = message_content.split(" ")
        user = args[-1]
        game = " ".join(args[:-1])

        if not UserManager.is_user_accepted(user):
            await MessageManager.send_error_message(ctx.channel, f"User {args[-1]} is no valid user.")
            return

        entry = BacklogEntry(game,UserManager.get_user_name(user),ctx.author.name)
        self.backlog_database.add_entry(entry)

        await MessageManager.send_message(ctx.channel, f"Recommended **{game}** to **{user}**.")

    def help(self) -> str:
        """
        Returns the help text for the recommend command.
        :return: The help text for the recommend command.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}recommend` `gameName` `user` - Recommends a game to another user\n"