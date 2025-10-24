from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.UserManager import UserManager

class PlayCommand(Command):
    async def execute(self, ctx):
        """
        Executes the PlayCommand.
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are not allowed to use this command.")
            return


    def help(self) -> str:
        """
        Returns a help string for the PlayCommand.
        :return: A string describing the PlayCommand.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}play` `url` : Plays audio from a YouTube URL in the voice channel you are connected to\n" +\
                f"- `{ConfigLoader.get_config().command_prefix}play` `videName` : Searches YouTube for the given video name and plays the first result in the voice channel you are connected to\n"
