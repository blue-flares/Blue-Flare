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
                # description = f'Command: \n```\n{ctx.command}```',
                color = discord.Color.red(),
                timestamp = discord.utils.utcnow()
            )
            """
            e.add_field(
                name = 'Type',
                value = f'```\n{type(error)}```',
                inline = False
            )
            e.add_field(
                name = 'Error',
                value = f'```\n{error}```',
                inline = False
            )
            e.add_field(
                name = 'Traceback',
                value = f'```\n{error.__traceback__}```',
                inline = False
            )
            e.add_field(
                name = 'File',
                value = f'```\n{sys.stderr}```',
                inline = False
            )"""
        
            etype = type(error)
            trace = error.__traceback__
            lines = traceback.format_exception(etype, error, trace)
            n_err = ''.join(lines)
            e.description = n_err
            
            await ctx.send(embed = e)

async def setup(bot):
    await bot.add_cog(Error(bot))