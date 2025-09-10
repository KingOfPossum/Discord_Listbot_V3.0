import os

from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.ImageLoader import ImageLoader
from common.Wrapper import Wrapper


class EmojiCreator:
    @staticmethod
    async def create_emoji_from_url(guild,emoji_name,url):
        """
        Creates a custom emoji in the specified guild from an image URL.
        :param guild: The guild in which to create the emoji.
        :param emoji_name: The name of the emoji to be created.
        :param url: The URL of the image to be used for the emoji.
        """
        print(url)
        ImageLoader.load_image(url,"temp.jpg")
        image = ImageLoader.convert_image_to_byte_array("temp.jpg")

        emoji = await guild.create_custom_emoji(name=emoji_name,image=image)
        os.remove("temp.jpg")

        return emoji

    @staticmethod
    async def create_console_emoji(guild,console_name,url):
        """
        Creates a console emoji in the specified guild from an image URL.
        :param guild: The guild in which to create the emoji.
        :param console_name: The name of the console emoji to be created.
        :param url: The URL of the image to be used for the console emoji.
        :return:
        """
        if ConfigLoader.get_config().create_emojis:
            emoji = await EmojiCreator.create_emoji_from_url(guild,console_name,url)
            Emojis.CONSOLES[console_name] = f"<:{emoji.name}:{emoji.id}>"
        else:
            Emojis.CONSOLES[console_name] = console_name
        ConfigLoader.update("consoles",Emojis.CONSOLES)

    @staticmethod
    async def create_console_emoji_if_not_exists(guild,console_name):
        if not await EmojiCreator.emoji_exists(guild, console_name):
            print("Creating Emoji")
            console_logo = Wrapper.request("platforms",
                                           f"fields platform_logo.url; where name ~ *\"{console_name}\"* | abbreviation ~ *\"{console_name}\"*;")
            await EmojiCreator.create_console_emoji(guild, console_name,
                                                    "https:" + console_logo[0]["platform_logo"]["url"].replace(
                                                        "t_thumb", "t_logo_med"))

    @staticmethod
    async def emoji_exists(guild,emoji_name):
        """
        Checks if an emoji with the specified name exists in the guild.
        :param guild: The guild to check for the emoji.
        :param emoji_name: The name of the emoji to check for.
        :return: True if it exists, False otherwise.
        """
        for emoji in guild.emojis:
            if emoji.name == emoji_name:
                return True
        return False