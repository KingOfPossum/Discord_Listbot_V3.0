import random

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from discord.ext import commands

class RandomizeCommand(Command):
    """
    Command to randomize an item from a provided list of items.
    """

    @commands.command(name="randomize",aliases=["Randomize","RANDOMIZE","rand","Rand","RAND","random","Random","RANDOM"])
    async def execute(self,ctx):
        """
        Randomizes an element from a provided list of items.
        """
        command_data = BotUtils.get_message_content(ctx.message)
        items = command_data.split(",")

        if len(items) == 0 or items[0] == "":
            await MessageManager.send_error_message(ctx.channel,"please Provide a List of Items separated by Commas")
            return

        await ctx.send(random.choice(items))

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"-  `{ConfigLoader.get_config().command_prefix}randomize` `item1`,`item2`,... - Returns a random item from the provided list of items.\n"