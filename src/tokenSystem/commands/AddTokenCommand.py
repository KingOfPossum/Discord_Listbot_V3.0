import discord

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.TokensDatabase import TokensDatabase
from discord.ext import commands

class AddTokenCommand(Command):
    """
    Command that will add a token to a user in the database.
    """
    def __init__(self,database: TokensDatabase):
        self.database = database

    @commands.command(name="addToken",aliases=["AddToken","addtoken","ADDTOKEN","add_token","Add_Token"])
    async def execute(self,ctx: discord.Interaction):
        """
        Handles the 'addToken' command to add a token to the database.
        This command will check if the user is authorized to use this command.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        await self.database.add_token(ctx.author.name,ctx)
        await MessageManager.send_message(ctx.channel,"Added token!")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}addToken` - Adds a token to your account.\n"