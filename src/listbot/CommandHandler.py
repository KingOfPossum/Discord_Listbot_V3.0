import discord

from common.BotUtils import BotUtils
from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.GameCreationModal import GameCreationModal
from common.GameEntry import GameEntry
from database.DatabaseCollection import DatabaseCollection

class CommandHandler:
    """
    A class that handles commands related to game management in a Discord bot.
    This class provides a static method to handle the 'add' command, which will prompt the user with a modal to fill in game details.
    """

    def __init__(self,databases: DatabaseCollection):
        self.databases = databases

    async def game_exists(self,ctx: discord.Interaction) -> tuple[str,GameEntry]:
        """
        Checks if a game exists in the database.
        :param ctx: The context in which the command was invoked
        :return: Tuple containing the game name and the GameEntry object if it exists, otherwise None.
        """
        game_name = BotUtils.get_message_content(ctx.message)
        game_entry = self.databases.list_database.get_game_entry(game_name, ctx.author.name)

        if game_entry is None:
            await ctx.send("**Game not found!**")
            return None
        else:
            print(f"\nFound GameEntry:\n {game_entry}\n")
            return game_name, game_entry

    async def add_command(self,ctx: discord.Interaction):
        """
        Handles the 'add' command to add a game to the list.
        Will show the user a modal to fill in the game details.
        :param interaction: The interaction in which the modal will be send.
        """
        add_button = discord.ui.Button(label="Add Game", style=discord.ButtonStyle.green)
        add_button.callback = lambda interaction: interaction.response.send_modal(GameCreationModal(self.databases.list_database))

        view = discord.ui.View()
        view.add_item(add_button)

        await ctx.send(view=view)

    async def update_command(self, ctx: discord.Interaction):
        """
        Handles the 'update' command to update an existing game in the list.
        This command will check if the game exists in the database and if it does, it will
        create a button that, when clicked, will open a GameCreationModal to update the game details.
        If the game does not exist, it will send a message indicating that the game was not found.
        :param ctx: The context in which the command was invoked
        """

        game = await self.game_exists(ctx)
        if game is None:
            return

        game_name, game_entry = game

        async def update_button_callback(interaction: discord.Interaction):
            modal = GameCreationModal(self.databases.list_database, game_entry)
            await interaction.response.send_modal(modal)

        update_button = discord.ui.Button(label="Update Game",style=discord.ButtonStyle.blurple)
        update_button.callback = update_button_callback

        view = discord.ui.View()
        view.add_item(update_button)

        await ctx.send(view=view)

    async def replayed_hundred_percent_command(self,ctx: discord.Interaction,replay: bool,hundred_percent: bool):
        """
        Handles the 'replayed' and 'completed' command to change either the replayed or completed status of a game.
        This command will check if the game exists in the database and if it does, it will
        change the replayed or completed status of the game.
        :param ctx: The context in which the command was invoked
        :param replay: Boolean indicating if replayed status should be changed
        :param hundred_percent: Boolean indicating if completed status should be changed
        """
        game = await self.game_exists(ctx)
        if game is None:
            return

        game_name, old_game_entry = game
        new_game_entry = old_game_entry

        if replay:
            new_game_entry.replayed = True if old_game_entry.replayed is False else False
            print(f"Replayed status changed to: {new_game_entry.replayed}\n")
        if hundred_percent:
            new_game_entry.hundred_percent = True if old_game_entry.hundred_percent is False else False
            print(f"Hundred percent status changed to: {new_game_entry.hundred_percent}\n")

        self.databases.list_database.put_game(new_game_entry, old_game_entry)

        emojis = [Emojis.CROSS_MARK, Emojis.CHECK_MARK]

        changed_var = "replayed" if replay else "completed"
        changed_var_value = new_game_entry.replayed if replay else new_game_entry.hundred_percent
        await ctx.send(f"**Changed {changed_var} status of {game_name} to: {emojis[changed_var_value]}**")

    async def help_command(self, ctx: discord.Interaction):
        command_prefix = ConfigLoader.load().command_prefix

        await ctx.send("**Available Commands:**\n"
                        f"`{command_prefix}add` - Add a new game to the list\n"
                        f"`{command_prefix}update` `gameName` - Update an existing game in the list\n"
                        f"`{command_prefix}replayed` `gameName` - Mark a game as replayed\n"
                        f"`{command_prefix}completed` `gameName` - Mark a game as completed (100%)\n")