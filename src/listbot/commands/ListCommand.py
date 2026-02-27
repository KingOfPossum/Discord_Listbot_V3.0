from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from discord.ext import commands
from listbot.GameList import GameList

class ListCommand(Command):
    """
    Command that will list all games of a specific user from the database.
    """

    @commands.command(name="list",aliases=["List","LIST","ls","LS","listGames","ListGames","LISTGAMES","list_games","List_Games","LIST_GAMES"])
    async def execute(self,ctx):
        """
        Handles the 'list' command to list all games of a specific user.
        This command will check if the user is accepted and if they are, it will
        retrieve and display the list of games for that user if no other user is provided.
        If there is another user provided, it will list the games for that user instead if this user itself is also accepted by the bot.
        :param ctx: the context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        user = BotUtils.get_message_content(ctx.message)
        if user == "":
            game_list = GameList(ctx)
        else:
            if not UserManager.is_user_accepted(user):
                await MessageManager.send_error_message(ctx.channel,"the Provided User is Not an Legal User")
                return

            # Accept both username and display name for the user
            user_entry = UserManager.get_user_entry(user_name=user)
            if not user_entry:
                user_entry = UserManager.get_user_entry(display_name=user)

            game_list = GameList(ctx,user=user_entry.user_name)

        await game_list.send_list(ctx.guild)

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"- `{ConfigLoader.get_config().command_prefix}list` - List all games from your list.\n" \
                f"- `{ConfigLoader.get_config().command_prefix}list` `user` - List all games from the users list.\n"