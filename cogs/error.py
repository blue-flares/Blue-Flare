import discord
from discord.ext import commands

import traceback
import sys

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            e = discord.Embed(
                title = 'Error Occured',
                description = f'{error}',
                color = discord.Color.red()
            )
            await ctx.send(embed = e)
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            e = discord.Embed(
                title = 'Error Occured',
                description = f'```\nType: {type(error)}\nError: {error}\nTraceback: {error.__traceback__}```',
                color = discord.Color.red()
            )
            await ctx.send(embed = e)

def setup(bot):
    bot.add_cog(Error(bot))