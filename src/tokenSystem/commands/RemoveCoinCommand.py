import discord

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.TokensEntry import TokensEntry
from common.UserManager import UserManager
from database.TokensDatabase import TokensDatabase
from discord.ext import commands

class RemoveCoinCommand(Command):
    """
    Command to remove a coin from a users account.
    """
    def __init__(self,database: TokensDatabase):
        self.database = database

    @commands.command(name="removeCoin")
    async def execute(self,ctx:discord.Interaction):
        """
        Handles the 'removeCoin' command to remove a coin from a user's account.
        :param ctx: The context in which the command was invoked
        """
        if ctx.author.name not in UserManager.accepted_users:
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        entry: TokensEntry = self.database.remove_coin(ctx.author.name)
        if entry:
            await MessageManager.send_message(ctx.channel,f"Removed a coin from your account. You now have {entry.coins} coins left.")
        else:
            await MessageManager.send_error_message(ctx.channel,"You Don't have any Coins to Remove")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}removeCoin` -Removes a coin from your account.\n"