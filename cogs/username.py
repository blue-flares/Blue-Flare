import discord
from discord.ext import commands

from utility import checks, embed
from utility.button import UsernameButton

import asyncio

class Username(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_editor()
    @commands.group(invoke_without_command = True, aliases = ('un',))
    async def username(self, ctx):
        """ Used to change the username of any user. """
        e = embed.error_embed(ctx, 'Please provide a subcommand. Available subcommands are: \n1.Set\n2.Reset')
        
        return await ctx.send(embed = e)

    @checks.is_editor()
    @username.command(aliases = ('s',))
    async def set(self, ctx, user: discord.Member = None, username: str = None):
        """ Used to set the username for a user. """
        if not user:
            return await ctx.send('Please provide the user.')
        if not username:
            return await ctx.send('Please provide the username.')
        
        e = embed.data_update(ctx, 'Username Update', discord.Color.red())
        e.description = 'The following things will be updated.'
        e.add_field(name = 'User', value = f'<@{user.id}>', inline = False)
        e.add_field(name = 'Value', value = username.title(), inline = False)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)
        
        await ctx.send(embed = e, view = UsernameButton(ctx, user, username, 'set', e))

    @checks.is_editor()
    @username.command(aliases = ('rs',))
    async def reset(self, ctx, user: discord.Member = None):
        """ Used to reset the username of a user. """
        if not user:
            return await ctx.send('Please provide the user.')
        
        e = embed.data_update(ctx, 'Username Update', discord.Color.red())
        e.description = 'The username of the user will be reseted.'
        e.add_field(name = 'User', value = f'<@{user.id}>', inline = False)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = UsernameButton(ctx, user, 'None', 'reset', e))

def setup(bot):
    bot.add_cog(Username(bot))