from common.BacklogEntry import BacklogEntry
from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.DatabaseCollection import DatabaseCollection
from discord.ext import commands

class RecommendCommand(Command):
    """
    A command to recommend a game to another user.
    """

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

        # Accept both username and display name for the user
        user_entry = UserManager.get_user_entry(user_name=user)
        if not user_entry:
            user_entry = UserManager.get_user_entry(display_name=user)

        entry = BacklogEntry(game,user_entry.user_id,ctx.author.id)
        DatabaseCollection.backlog_database.add_entry(entry)

        await MessageManager.send_message(ctx.channel, f"Recommended **{game}** to **{user}**.")

    def help(self) -> str:
        """
        Returns the help text for the recommend command.
        :return: The help text for the recommend command.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}recommend` `gameName` `user` - Recommends a game to another user\n"