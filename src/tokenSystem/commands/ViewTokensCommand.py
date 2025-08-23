import discord

from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.TokensDatabase import TokensDatabase
from discord.ext import commands

class ViewTokensCommand(Command):
    """
    Command to view infos about your tokens and coins.
    """
    def __init__(self,database: TokensDatabase):
        self.database = database

    @commands.command(name="viewTokens",aliases=["tokens"])
    async def execute(self,ctx:discord.Interaction):
        """
        Handles the 'viewTokens' command to view infos about your tokens and coins.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        entry = self.database.get_tokens_entry(ctx.author.name)
        if not entry:
            await MessageManager.send_error_message(ctx.channel,"No entry in tokens database found!")

        tokens_view_txt = f"Current Tokens: {entry.tokens % entry.needed_tokens}\n" \
                            f"Total Tokens: {entry.tokens}\n" \
                            f"Coins: {entry.coins}\n" \
                            f"Tokens needed for next coin: {entry.needed_tokens - (entry.tokens % entry.needed_tokens)}"
        embed = MessageManager.get_embed(title=f"{ctx.author.display_name}'s Tokens Info",description=tokens_view_txt,user=ctx.author)
        await MessageManager.send_message(ctx.channel,embed=embed)

    def help(self) -> str:
        """
        Provides help information for the command.
        :return: A string containing the help information.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}viewTokens` - View infos about your tokens and coins.\n"