import random

from common.Command import Command
from discord.ext import commands
from common.BotUtils import BotUtils
from common.ConfigLoader import ConfigLoader

class RandomizeNumCommand(Command):
    """
    Command to randomize a number.
    """

    @commands.command(name="randomizeNum")
    async def execute(self,ctx):
        """
        Randomizes a number between two provided numbers.
        :param ctx: The context in which the command was invoked.
        """
        command_data = BotUtils.get_message_content(ctx.message)

        nums = command_data.split(",")
        if 0 > len(nums) > 2:
            await ctx.send("Please provide only one or two numbers separated by a comma.")
            return

        try:
            num1 = 1 if len(nums) == 1 else int(nums[1])
            num2 = int(nums[0]) if len(nums) == 1 else int(nums[1])

            if num1 > num2:
                await ctx.send("The first number must be less than or equal to the second number.")
                return

            random_num = random.randint(num1,num2)
            await ctx.send(random_num)
        except ValueError:
            await ctx.send("Please provide valid numbers.")

    def help(self) -> str:
        """
        Returns a string that describes the command and how to use it.
        :return: The help string for the command
        """
        return f"-  `{ConfigLoader.get_config().command_prefix}randomizeNum` `num1`,`num2` - Randomizes a number between `num1` and `num2` if you only provide one number `num1` will be 1.\n"