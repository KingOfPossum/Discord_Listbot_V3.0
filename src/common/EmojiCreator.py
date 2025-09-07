import os

from common.ConfigLoader import ConfigLoader
from common.Emojis import Emojis
from common.ImageLoader import ImageLoader

class EmojiCreator:
    @staticmethod
    async def create_emoji_from_url(guild,emoji_name,url):
        """
        Creates a custom emoji in the specified guild from an image URL.
        :param guild: The guild in which to create the emoji.
        :param emoji_name: The name of the emoji to be created.
        :param url: The URL of the image to be used for the emoji.
        """
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