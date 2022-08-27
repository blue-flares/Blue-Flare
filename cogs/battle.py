import discord
from discord.ext import commands

from utility import checks, embed
from utility.button import BattleButton

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_editor()
    @commands.group(invoke_without_command = True, aliases = ('bt',))
    async def battle(self, ctx):
        """ Used to change Battle value for many users. """
        e = embed.error_embed(ctx, 'Please provide a subcommand. Available subcommands are: \n1.Add\n2.Remove\n3.Set\n4.Reset')

        await ctx.send(embed = e)

    @battle.command(aliases = ('a',))
    async def add(self, ctx, result: str = None, members: commands.Greedy[discord.Member] = None, value: int = None):
        """
        Used to add value to result for specified users.

        Parameters:
            result = Choose from win, lose, draw.
            members = Specify one or many discord users.
            value = The value to add. 
        """
        e = embed.error_embed(ctx, 'Invalid syntax')
        e.add_field(name = 'Description', value = 'Used to add [win|lose|draw] to specified users.')
        e.add_field(name = 'Correct Syntax', value = '```\nbf [battle|bt] [add|a] [result] [members] [value]```', inline = False)
        e.add_field(name = 'Example', value = f'bf battle add win <@{self.bot.user.id}> 1', inline = False)
        
        if not result:
            return await ctx.send(embed = e)
        if not members:
            return await ctx.send(embed = e)
        if not value:
            return await ctx.send(embed = e)

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Battle Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Battle Added', value = f'{value}', inline = True)
        e.add_field(name = 'Result', value = f'{result.title()}', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = BattleButton(ctx, user, value, 'add', e, result))

    @battle.command(aliases = ('r',))
    async def remove(self, ctx, result: str = None, members: commands.Greedy[discord.Member] = None, value: int = None):
        """
        Used to remove value from result for specified users.

        Parameters:
            result = Choose from win, lose, draw.
            members = Specify one or many discord users.
            value = The value to remove. 
        """
        e = embed.error_embed(ctx, 'Invalid syntax')
        e.add_field(name = 'Description', value = 'Used to remove [win|lose|draw] to specified users.')
        e.add_field(name = 'Correct Syntax', value = '```\nbf [battle|bt] [remove|r] [result] [members] [value]```', inline = False)
        e.add_field(name = 'Example', value = f'bf battle remove win <@{self.bot.user.id}> 1', inline = False)
        
        if not result:
            return await ctx.send(embed = e)
        if not members:
            return await ctx.send(embed = e)
        if not value:
            return await ctx.send(embed = e)

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Battle Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Battle Remove', value = f'{value}', inline = True)
        e.add_field(name = 'Result', value = f'{result.title()}', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = BattleButton(ctx, user, value, 'remove', e, result))

    @battle.command(aliases = ('s',))
    async def set(self, ctx, result: str = None, members: commands.Greedy[discord.Member] = None, value: int = None):
        """
        Used to set value to result for specified users.

        Parameters:
            result = Choose from win, lose, draw.
            members = Specify one or many discord users.
            value = The value to set. 
        """
        e = embed.error_embed(ctx, 'Invalid syntax')
        e.add_field(name = 'Description', value = 'Used to set [win|lose|draw] to specified users.')
        e.add_field(name = 'Correct Syntax', value = '```\nbf [battle|bt] [set|s] [result] [members] [value]```', inline = False)
        e.add_field(name = 'Example', value = f'bf battle set win <@{self.bot.user.id}> 1', inline = False)
        
        if not result:
            return await ctx.send(embed = e)
        if not members:
            return await ctx.send(embed = e)
        if not value:
            return await ctx.send(embed = e)

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Battle Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Battle set', value = f'{value}', inline = True)
        e.add_field(name = 'Result', value = f'{result.title()}', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = BattleButton(ctx, user, value, 'set', e, result))

    @battle.command(aliases = ('rs',))
    async def reset(self, ctx, result: str = None, members: commands.Greedy[discord.Member] = None):
        """
        Used to reset result for specified users.

        Parameters:
            result = Choose from win, lose, draw.
            members = Specify one or many discord users.
        """
        e = embed.error_embed(ctx, 'Invalid syntax')
        e.add_field(name = 'Description', value = 'Used to reset [win|lose|draw] to specified users.')
        e.add_field(name = 'Correct Syntax', value = '```\nbf [battle|bt] [reset|rs] [result] [members]```', inline = False)
        e.add_field(name = 'Example', value = f'bf battle reset win <@{self.bot.user.id}> ', inline = False)
        
        if not result:
            return await ctx.send(embed = e)
        if not members:
            return await ctx.send(embed = e)

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Battle Update', discord.Color.red())
        e.description = 'Following things will be reset.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Result', value = f'{result.title()}', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = BattleButton(ctx, user, 0, 'reset', e, result))

def setup(bot):
    bot.add_cog(Battle(bot))
