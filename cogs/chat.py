import discord
from discord.ext import commands

from utility import checks, embed
from utility.button import ChatButton

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_editor()
    @commands.group(invoke_without_command = True)
    async def chat(self, ctx):
        """ Used to change the top weekly chat winners for many user. """
        e = embed.error_embed(ctx, 'Please provide a subcommand. Available subcommands are: \n1.Add\n2.Remove\n3.Set\n4.Reset')

        await ctx.send(embed = e)

    @chat.command(aliases = ('a',))
    async def add(self, ctx, members: commands.Greedy[discord.Member] = None, value: int = None):
        """ Used to add value to specified users. """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not value:
            return await ctx.send('Please provide the value to add.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Chat Value', value = f'{value}', inline = True)
        e.add_field(name = 'Mode', value = 'Add', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = ChatButton(ctx, user, value, 'add', e))

    @chat.command(aliases = ('r',))
    async def remove(self, ctx, members: commands.Greedy[discord.Member] = None, value: int = None):
        """ Used to remove value from specified users. """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not value:
            return await ctx.send('Please provide the value to remove.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Chat Value', value = f'{value}', inline = True)
        e.add_field(name = 'Mode', value = 'Remove', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = ChatButton(ctx, user, value, 'remove', e))

    @chat.command(aliases = ('s',))
    async def set(self, ctx, members: commands.Greedy[discord.Member] = None, value: int = None):
        """ Used to set donation as specified for specified users.  """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not value:
            return await ctx.send('Please provide the value to set.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Chat Value', value = f'{value}', inline = True)
        e.add_field(name = 'Mode', value = 'Set', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = ChatButton(ctx, user, value, 'set', e))

    @chat.command(aliases = ('rs',))
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

        await ctx.send(embed = e, view = ChatButton(ctx, user, 0, 'reset', e))

async def setup(bot):
    await bot.add_cog(Chat(bot))