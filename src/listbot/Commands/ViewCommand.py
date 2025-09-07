from common.BotUtils import BotUtils
from common.Command import Command
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.GameEntry import GameEntry
from common.MessageManager import MessageManager
from common.UserManager import UserManager
from database.ListDatabase import ListDatabase
from discord.ext import commands
from Game import Game
from wrapper import IGDBWrapper

class ViewCommand(Command):
    """
    Command to view game details from a specific game
    Supports both own user and other users
    """
    def __init__(self,database: ListDatabase):
        self.database = database

        self.wrapper = IGDBWrapper("vhxxz4jvptvoj99f6arnjii3wgzq47",
                                   "ydclz2x5k42rru95bzgr6kqvxfmum9")

    @staticmethod
    def get_game_view_txt(game_entry: GameEntry, game_data: Game) -> str:
        """
        Creates an embed for the game view command.
        Contains all information about the game entry.
        :param game_data: The IGDB Game object containing additional game details.
        :param game_entry: The GameEntry containing the game details.
        :return : A formatted string with the game details.
        """
        console_emoji = Emojis.CONSOLES[game_entry.console] if Emojis.CONSOLES[
                                                                   game_entry.console] != "" else game_entry.console

        view_game_details = f"**Console:** {console_emoji}\n" \
                            f"**Rating:** {game_entry.rating}\n" \
                            f"**Genre:** {", ".join([genre for genre in game_data.genres[0]] if game_data else "IDK")}\n" \
                            f"**Review:** {game_entry.review}\n\n" \
                            f"**Replay:** {[Emojis.CROSS_MARK, Emojis.CHECK_MARK][game_entry.replayed]}\n\n" \
                            f"Added on **{game_entry.date}**"

        return view_game_details


    @commands.command(name="view",aliases=["View","v","viewGame","ViewGame","VIEW","VIEWGAME","view_game","View_Game","VIEW_GAME","viewgame","Viewgame"])
    async def execute(self, ctx):
        """
        Handles the 'view' command to view the game details of a specific game.
        This command will check if the game exists in the database and then display its details.
        If the game does not exist, it will send an error message.
        :param ctx: The context in which the command was invoked
        """
        if not UserManager.is_user_accepted(ctx.author.name):
            await MessageManager.send_error_message(ctx.channel,"You are Not Allowed to use this command")
            return

        args = BotUtils.get_message_content(ctx.message).split()
        if not args:
            await MessageManager.send_error_message(ctx.channel,"Please Provide a Game Name")
            return

        if len(args) > 1 and UserManager.is_user_accepted(args[-1]):
            user = args[-1]
            game_name = " ".join(args[:-1])
        else:
            user = None
            game_name = " ".join(args)

        game = await BotUtils.game_exists(game_name,self.database,user=user,ctx=ctx)
        if not game:
            return

        game_name, game_entry = game

        game_infos = Game.from_igdb(self.wrapper,game_name,game_entry.console)

        embed = MessageManager.get_embed(title=f"**{game_name} {"(100%)" * game_entry.hundred_percent}**",description=self.get_game_view_txt(game_entry,game_infos))
        embed.set_thumbnail(url=game_infos.cover)

        await MessageManager.send_message(ctx.channel,embed=embed)

    def help(self) -> str:
        return f"- `{ConfigLoader.get_config().command_prefix}view` `gameName` - View the details of a game your list\n" \
               f"- `{ConfigLoader.get_config().command_prefix}view` `gameName` `user` - View the details of a game from another user's list\n"