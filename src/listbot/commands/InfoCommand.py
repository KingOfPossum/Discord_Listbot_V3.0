from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager
from common.TimeUtils import TimeUtils
from common.Wrapper import Wrapper
from discord.ext import commands
from Game import Game

class InfoCommand(Command):
    """Command to get more information's about a specific game using the IGDB database."""

    @commands.command(name="info",aliases=["i","INFO","gameinfo","GameInfo","GAMEINFO","game_info","Game_Info","GAME_INFO"])
    async def execute(self, ctx):
        """
        Handles the 'info' command to get more information's about a specific game.
        This command will look for information's about a specific game in the IGDB database and will send them in an embed message.
        :param ctx: the context in which the command was invoked
        """
        game_name = BotUtils.get_message_content(ctx.message)
        game = Game.from_igdb(Wrapper.wrapper,game_name,load_all=True)

        embed = MessageManager.get_embed(title=f"**{game_name}**",description=f"**Description:**\n{game.summary}\n**Genres:**\n{", ".join(game.genres)}\n**Platforms:**\n{", ".join(game.platforms)}\n**Release Date:**\n{TimeUtils.timestamp_to_date(min(game.release_dates))}")
        embed.set_thumbnail(url=game.cover)
        await MessageManager.send_message(ctx.channel,embed=embed)

    def help(self) -> str:
        return f"- `{ConfigLoader.get_config().command_prefix}info` `gameName` - Get more information's about a specific game.\n"