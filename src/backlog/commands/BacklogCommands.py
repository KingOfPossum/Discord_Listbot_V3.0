from backlog.commands.BacklogAddCommand import BacklogAddCommand
from backlog.commands.BacklogRemoveCommand import BacklogRemoveCommand
from backlog.commands.GetRecommendationCommand import GetRecommendationCommand
from backlog.commands.RecommendCommand import RecommendCommand
from backlog.commands.ViewBacklogCommand import ViewBacklogCommand
from database.DatabaseCollection import DatabaseCollection

class BacklogCommands:
    """
    Collection of commands related to backlog management.
    This class registers these commands to the provided bot instance.
    """

    async def register(self,bot):
        """
        Registers the backlog commands with the provided bot.
        :param bot: The Discord bot instance to register commands with.
        """
        await bot.add_cog(BacklogAddCommand())
        await bot.add_cog(BacklogRemoveCommand())
        await bot.add_cog(ViewBacklogCommand())
        await bot.add_cog(RecommendCommand())
        await bot.add_cog(GetRecommendationCommand())

        print("Registered BacklogCommands cogs.")