import random

from common.Command import Command
from discord.ext import commands
from common.BotUtils import BotUtils
from common.ConfigLoader import ConfigLoader
from common.MessageManager import MessageManager

class RandomizeNumCommand(Command):
    """
    Command to randomize a number.
    """

    @commands.command(name="randomizeNum",aliases=["RandomizeNum","RANDOMIZENUM","randNum","RandNum","RANDNUM","randomNum","RandomNum","RANDOMNUM","randomizeNumber","RandomizeNumber","RANDOMIZENUMBER"])
    async def execute(self,ctx):
        """
        Randomizes a number between two provided numbers.
        :param ctx: The context in which the command was invoked.
        """
        command_data = BotUtils.get_message_content(ctx.message)

        nums = command_data.split(",")

        if len(nums) <= 0 or len(nums) > 2:
            await MessageManager.send_error_message(ctx.channel,"please provide only One or Two numbers separated by a comma")
            return

        try:
            num1 = 1 if len(nums) == 1 else int(nums[0])
            num2 = int(nums[0]) if len(nums) == 1 else int(nums[1])

            if num1 > num2:
                await MessageManager.send_error_message(ctx.channel,"the First number must be Less Than or Equal to the Second number")
                return

            random_num = random.randint(num1,num2)
            await ctx.send(random_num)
        except ValueError:
            await MessageManager.send_error_message(ctx.channel,"please provide Valid Numbers")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"-  `{ConfigLoader.get_config().command_prefix}randomizeNum` `num1`,`num2` - Randomizes a number between `num1` and `num2` if you only provide one number `num1` will be 1.\n"