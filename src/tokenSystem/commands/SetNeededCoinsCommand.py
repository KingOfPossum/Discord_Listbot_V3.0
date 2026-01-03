import discord

from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.TokensDatabase import TokensDatabase
from discord.ext import commands

class SetNeededCoinsCommand(Command):
    """
    Command to set the number of tokens needed to earn a coin for a user.
    """
    def __init__(self,database: TokensDatabase):
        self.database = database

    @commands.command(name="setNeededTokens",aliases=["neededTokens","setneededtokens","SETNEEDEDTOKENS","SetNeededTokens","set_needed_tokens","Set_Needed_Tokens","SET_NEEDED_TOKENS"])
    async def execute(self,ctx:discord.Interaction):
        """
        Handles the 'setNeededTokens' command to set the number of tokens needed to earn a coin for a user.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        needed_tokens_str = BotUtils.get_message_content(ctx.message)
        try:
            needed_tokens = int(needed_tokens_str)
            self.database.set_needed_tokens(ctx.author.name,needed_tokens)
            await MessageManager.send_message(ctx.channel,f"Needed Tokens set to {needed_tokens}")
        except ValueError:
            await MessageManager.send_error_message(ctx.channel,"Please Provide a Valid Number.")
            return

    def help(self) -> str:
        """
        Provides help information for the command.
        :return: A string containing the help information.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}setNeededTokens` `number` - Sets the number of tokens needed for you to earn a coin to `number`.\n"