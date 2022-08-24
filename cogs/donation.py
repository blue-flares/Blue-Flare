import discord
from discord.ext import commands

from utility import embed, checks
from utility.button import DonationButton

import asyncio

class Donation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_editor()
    @commands.group(invoke_without_command = True, aliases = ('do'))
    async def donation(self, ctx):
        """ Used to change the donation values for many user. """
        e = embed.error_embed(ctx, 'Please provide a subcommand. Available subcommands are: \n1.Add\n2.Remove\n3.Set\n4.Reset')

        await ctx.send(embed = e)

    @donation.command(aliases = ('a'))
    async def add(self, ctx, members: commands.Greedy[discord.Member] = None, donation: int = None):
        """ Used to add donation to specified users. """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not donation:
            return await ctx.send('Please provide the donation to add.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Donation', value = f'{donation}m', inline = True)
        e.add_field(name = 'Mode', value = 'Add', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = DonationButton(ctx, user, donation, 'add', e))

    @donation.command(aliases = ('r'))
    async def remove(self, ctx, members: commands.Greedy[discord.Member] = None, donation: int = None):
        """ Used to remove donation from specified users. """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not donation:
            return await ctx.send('Please provide the donation to remove.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Donation', value = f'{donation}m', inline = True)
        e.add_field(name = 'Mode', value = 'Remove', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = DonationButton(ctx, user, donation, 'remove', e))

    @donation.command(aliases = ('s'))
    async def set(self, ctx, members: commands.Greedy[discord.Member] = None, donation: int = None):
        """ Used to set donation as specified for specified users.  """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not donation:
            return await ctx.send('Please provide the donation to set.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Donation', value = f'{donation}m', inline = True)
        e.add_field(name = 'Mode', value = 'Set', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = DonationButton(ctx, user, donation, 'set', e))

    @donation.command(aliases = ('rs'))
    async def reset(self, ctx, members: commands.Greedy[discord.Member] = None):
        """ Used to reset the donation to 0 for specifies members. """
        if not members:
            return await ctx.send('Please provide the member(s).')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Mode', value = 'Reset', inline = False)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = DonationButton(ctx, user, 0, 'reset', e))
   
def setup(bot):
    bot.add_cog(Donation(bot))