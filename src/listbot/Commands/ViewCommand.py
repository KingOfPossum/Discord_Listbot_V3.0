from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.MessageManager import MessageManager
from database.Database import Database
from discord.ext import commands

class ViewCommand(Command):

    def __init__(self,database: Database):
        self.database = database

    @commands.command(name="view")
    async def execute(self, ctx):
        game = await BotUtils.game_exists(ctx,self.database)
        if not game:
            return

        game_name, game_entry = game

        view_game_details = f"**Console:** {game_entry.console}\n" \
                            f"**Rating:** {game_entry.replayed}\n" \
                            f"**Genre:** {game_entry.genre}\n" \
                            f"**Review:** {game_entry.review}\n\n" \
                            f"**Replay:** {[Emojis.CROSS_MARK, Emojis.CHECK_MARK][game_entry.replayed]}\n\n" \
                            f"Added on **{game_entry.date}**"
        await MessageManager.send_embed_message(ctx, f"**{game_name} {"(100%)" * game_entry.hundred_percent}**", view_game_details)

    def help(self) -> str:
        return f"- `{ConfigLoader.get_config().command_prefix}view` `gameName` - View the details of a game in the list\n"