import random

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database_.BacklogDatabase import BacklogDatabase
from discord.ext import commands

class GetRecommendationCommand(Command):
    """
    A command to get a game recommendation from your backlog.
    """
    def __init__(self, backlog_database:BacklogDatabase):
        self.backlog_database = backlog_database

    @commands.command(name="getRecommendation",aliases=["GetRecommendation","get_recommendation","GET_RECOMMENDATION","Get_Recommendation","getrecommendation","recommendation","Recommendation","RECOMMENDATION"])
    async def execute(self, ctx):
        """
        Gets a random game recommendation from the backlog of the command invoker.
        :param ctx: The context of the command.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        entries = self.backlog_database.get_all_entries(ctx.author.name)
        random_index = random.randint(0, len(entries) - 1)

        await MessageManager.send_message(ctx.channel, f"Your random game recommendation is: **{entries[random_index].name}**")

    def help(self) -> str:
        """
        Returns the help text for the get recommendation command.
        :return: The help text for the get recommendation command.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}getRecommendation` - Returns a random game recommendation from your backlog.\n"