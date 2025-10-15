from common.Command import Command
from common.ConfigLoader import ConfigLoader

class BacklogAddCommand(Command):
    """
    Command for adding games into the backlog.
    """
    async def execute(self, ctx):
        """
        Adds the provided game into the backlog of the command invoker.
        If the game is already in the backlog, nothing will be changed.
        :param ctx: The context of the command.
        """
        pass

    def help(self) -> str:
        """
        Provides help information for the command.
        :return: The help string for the command.
        """
        return f"- `{ConfigLoader.get_config().command_prefix}backlogAdd` `gameName` - Adds the game to your backlog\n"