import random

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from discord.ext import commands

class RandomizeCommand(Command):
    """
    Command to randomize an item from a provided list of items.
    """

    @commands.command(name="randomize")
    async def execute(self,ctx):
        """
        Randomizes an element from a provided list of items.
        """
        command_data = BotUtils.get_message_content(ctx.message)
        items = command_data.split(",")

        if len(items) == 0:
            await ctx.send("Please provide a list of items separated by commas.")
            return

        await ctx.send(random.choice(items))

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"-  `{ConfigLoader.get_config().command_prefix}randomize` `item1`,`item2`,... - Randomizes an item from the provided list of items.\n"